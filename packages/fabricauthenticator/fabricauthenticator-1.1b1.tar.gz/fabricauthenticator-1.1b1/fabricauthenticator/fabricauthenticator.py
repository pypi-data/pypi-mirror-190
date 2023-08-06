"""FabricAuthenticator for Jupyterhub

Based on CILogon authentication,
in addition checks if user belongs to Fabric JUPYTERHUB COU.

"""
import os
import traceback

import oauthenticator
from tornado import web
from ldap3 import Connection, Server, ALL


JUPYTERHUB_COU = os.getenv('FABRIC_COU_JUPYTERHUB', 'CO:COU:Jupyterhub:members:active')


class FabricAuthenticator(oauthenticator.CILogonOAuthenticator):
    """ The FabricAuthenticator inherits from CILogonAuthenticator.
    """
    async def authenticate(self, handler, data=None):
        """ First invoke CILogon authenticate method,
            then check if user has JUPYTERHUB_COU attribute.
        """
        userdict = await super(FabricAuthenticator, self).authenticate(handler, data)
        # check COU
        user_email = userdict["auth_state"]["cilogon_user"]["email"]
        if not self.is_in_allowed_cou(user_email):
            self.log.warn("FABRIC user {} is not in {}".format(userdict["name"], JUPYTERHUB_COU))
            raise web.HTTPError(403, "Access not allowed")
        self.log.debug("FABRIC user authenticated")
        return userdict

    async def pre_spawn_start(self, user, spawner):
        """ Populate credentials to spawned notebook environment
        """
        auth_state = await user.get_auth_state()
        self.log.debug("pre_spawn_start: {}".format(user.name))
        if not auth_state:
            return
        spawner.environment['CILOGON_ID_TOKEN'] \
            = auth_state['token_response'].get('id_token', '')
        spawner.environment['CILOGON_REFRESH_TOKEN'] \
            = auth_state['token_response'].get('refresh_token', '')
        self.log.info(f"FABRIC {user} token: {auth_state['token_response'].get('refresh_token', '')}")
        # setup environment
        nb_user = str(user.name)
        if "@" in nb_user:
            nb_user = nb_user.split("@", 1)[0]
        spawner.environment['NB_USER'] = nb_user
        self.log.debug(f"Environment: {spawner.environment}")

    async def refresh_user(self, user, handler=None):
        """ Force refresh of auth prior to spawn
        (based on setting c.Authenticator.refresh_pre_spawn = True)
        to ensure that user get a new refresh token.
        """
        self.log.info(f"[refresh_user] always trigger refresh authentication - {user}")
        try:
            await handler.stop_single_user(user, user.spawner.name)
            handler.clear_cookie("jupyterhub-hub-login")
            handler.clear_cookie("jupyterhub-session-id")
            handler.redirect('/hub/logout')
        except Exception as e:
            self.log.error(f"Error occurred while refreshing user - {user}; error: {e}")
            self.log.error(traceback.format_exc())
        return True

    def is_in_allowed_cou(self, email):
        """ Checks if user is in Comanage JUPYTERHUB COU.

            Args:
                email: i.e. email

            Returns:
                Boolean value: True if username has attribute of JUPYTERHUB_COU, False otherwise
        """
        attributelist = self.get_ldap_attributes(email)
        if attributelist:
            self.log.debug("attributelist acquired.")
            if attributelist['isMemberOf']:
                for attribute in attributelist['isMemberOf']:
                    if attribute == JUPYTERHUB_COU:
                        return True
        return False

    @staticmethod
    def get_ldap_attributes(email):
        """ Get the ldap attributes from Fabric CILogon instance.

            Args:
                email: i.e. email

            Returns:
                The attributes list
        """
        server = Server(os.getenv('LDAP_HOST', ''), use_ssl=True, get_info=ALL)
        ldap_user = os.getenv('LDAP_USER', '')
        ldap_password = os.getenv('LDAP_PASSWORD', '')
        ldap_search_base = os.getenv('LDAP_SEARCH_BASE', '')
        ldap_search_filter = '(mail=' + email + ')'
        conn = Connection(server, ldap_user, ldap_password, auto_bind=True)
        profile_found = conn.search(ldap_search_base,
                                    ldap_search_filter,
                                    attributes=[
                                        'isMemberOf',
                                    ])
        if profile_found:
            attributes = conn.entries[0]
        else:
            attributes = []
        conn.unbind()
        return attributes
