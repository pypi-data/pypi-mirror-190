from ck8s.helpers import ok, error, title
from ck8s.action import Action

from kubernetes import client, config


class TestAction(Action) :

  def __init__(self, args):
      super().__init__()
      self.args = args
      self.parseComponent()

  def parseComponent(self):
    cluster = self.args['cluster']
    component = self.args['component']

    config.load_kube_config(config_file="{}/.state/kube_config_{}.yaml".format(self.CK8S_CONFIG_PATH, cluster))
    appsV1 = client.AppsV1Api()

    if component is None :
      error("Please choose a component to test, list of valid components is : base, opensearch or ingress")
    elif component == 'base':
      title('Running base tests ...')
    elif component == 'opensearch':
      title('Running opensearch tests ... ')
    elif component == 'ingress':
      title('Running ingress tests')
      ret = appsV1.read_namespaced_daemon_set_status("ingress-nginx-controller", "ingress-nginx")
      if ret.status.number_ready != ret.status.desired_number_scheduled:
        error('[ERROR] Some ingress-nginx pods are not ready.')
      else :
        ok('[SUCCESS] All nginx pods are ready')


