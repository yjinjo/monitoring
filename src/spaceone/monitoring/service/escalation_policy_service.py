import logging

from spaceone.core.service import *
from spaceone.monitoring.model.escalation_policy_model import *
from spaceone.monitoring.manager.identity_manager import IdentityManager
from spaceone.monitoring.manager.escalation_policy_manager import EscalationPolicyManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class EscalationPolicyService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.escalation_policy_mgr: EscalationPolicyManager = self.locator.get_manager('EscalationPolicyManager')

    @transaction(append_meta={
        'authorization.scope': 'PROJECT',
        'authorization.require_project_id': True
    })
    @check_required(['name', 'rules', 'domain_id'])
    def create(self, params):
        """Create escalation policy

        Args:
            params (dict): {
                'name': 'str',
                'rules': 'list',
                'repeat_count': 'int',
                'finish_condition': 'str',
                'project_id': 'str',
                'tags': 'dict',
                'domain_id': 'str'
            }

        Returns:
            escalation_policy_vo (object)
        """

        project_id = params['project_id']
        domain_id = params['domain_id']

        identity_mgr: IdentityManager = self.locator.get_manager('IdentityManager')

        if project_id:
            identity_mgr.get_project(project_id, domain_id)
            params['scope'] = 'PROJECT'
        else:
            params['scope'] = 'GLOBAL'

        return self.escalation_policy_mgr.create_escalation_policy(params)

    @transaction(append_meta={'authorization.scope': 'PROJECT'})
    @check_required(['escalation_policy_id', 'domain_id'])
    def update(self, params):
        """Update escalation policy

        Args:
            params (dict): {
                'escalation_policy_id': 'dict',
                'name': 'str',
                'rules': 'list',
                'repeat_count': 'int',
                'finish_condition': 'str',
                'tags': 'dict',
                'domain_id': 'str'
            }

        Returns:
            escalation_policy_vo (object)
        """

        escalation_policy_id = params['escalation_policy_id']
        domain_id = params['domain_id']

        escalation_policy_vo = self.escalation_policy_mgr.get_escalation_policy(escalation_policy_id, domain_id)
        return self.escalation_policy_mgr.update_escalation_policy_by_vo(params, escalation_policy_vo)

    @transaction(append_meta={'authorization.scope': 'PROJECT'})
    @check_required(['escalation_policy_id', 'domain_id'])
    def set_default(self, params):
        """ Get escalation policy

        Args:
            params (dict): {
                'escalation_policy_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            escalation_policy_vo (object)
        """

        return self.escalation_policy_mgr.set_default_escalation_policy(params)

    @transaction(append_meta={'authorization.scope': 'PROJECT'})
    @check_required(['escalation_policy_id', 'domain_id'])
    def delete(self, params):
        """Delete escalation policy

        Args:
            params (dict): {
                'escalation_policy_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            None
        """

        self.escalation_policy_mgr.delete_escalation_policy(params['escalation_policy_id'], params['domain_id'])

    @transaction(append_meta={'authorization.scope': 'PROJECT'})
    @check_required(['escalation_policy_id', 'domain_id'])
    def get(self, params):
        """ Get escalation policy

        Args:
            params (dict): {
                'escalation_policy_id': 'str',
                'domain_id': 'str',
                'only': 'list
            }

        Returns:
            escalation_policy_vo (object)
        """

        return self.escalation_policy_mgr.get_escalation_policy(params['escalation_policy_id'],
                                                                params['domain_id'], params.get('only'))

    @transaction(append_meta={
        'authorization.scope': 'PROJECT',
        'mutation.append_parameter': {'user_projects': 'authorization.projects'}
    })
    @check_required(['domain_id'])
    @append_query_filter(['escalation_policy_id', 'name', 'is_default', 'finish_condition', 'scope',
                          'project_id', 'domain_id', 'user_projects'])
    @append_keyword_filter(['escalation_policy_id', 'name'])
    def list(self, params):
        """ List data sources

        Args:
            params (dict): {
                'escalation_policy_id': 'str',
                'name': 'str',
                'is_default': 'bool',
                'finish_condition': 'str',
                'scope': 'str',
                'project_id': 'str',
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.Query)',
                'user_projects': 'list', // from meta
            }

        Returns:
            escalation_policy_vos (object)
            total_count
        """

        query = params.get('query', {})
        return self.escalation_policy_mgr.list_escalation_policies(query)

    @transaction(append_meta={
        'authorization.scope': 'PROJECT',
        'mutation.append_parameter': {'user_projects': 'authorization.projects'}
    })
    @check_required(['query', 'domain_id'])
    @append_query_filter(['domain_id', 'user_projects'])
    @append_keyword_filter(['escalation_policy_id', 'name'])
    def stat(self, params):
        """
        Args:
            params (dict): {
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)',
                'user_projects': 'list', // from meta
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        query = params.get('query', {})
        return self.escalation_policy_mgr.stat_escalation_policies(query)
