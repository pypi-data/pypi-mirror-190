import json,logging,urllib.parse,requests,werkzeug.exceptions
from localstack.http import route
from localstack.utils.files import load_file
from werkzeug import Request,Response
from werkzeug.exceptions import BadRequest,InternalServerError
from localstack_ext.bootstrap.pods.launchpad.cache import CloudPodsCache,get_url_digest
from localstack_ext.bootstrap.pods_client import inject_pod_endpoint,read_metadata_from_pod
from localstack_ext.constants import API_PATH_PODS
LOG=logging.getLogger(__name__)
LAUNCHPAD_PATH=f"{API_PATH_PODS}/launchpad"
class LaunchPadApi:
	pods_cache:CloudPodsCache
	def __init__(A):A.pods_cache=CloudPodsCache()
	@route(f"{LAUNCHPAD_PATH}/fetch",methods=['POST'])
	def launchpad_fetch(self,request):
		try:A=unquote_and_validate_url(request)
		except werkzeug.exceptions.HTTPException as B:return Response(B.description,B.code)
		D=get_url_digest(A);C=self.pods_cache.update_cache(D);LOG.debug("Fetching Pod's content from %s to %s",A,C)
		def E():
			B=requests.get(A,stream=True);F=int(B.headers['Content-Length']);D=0
			with open(C,'wb')as G:
				for E in B.iter_content(chunk_size=100000):D+=len(E);G.write(E);yield f"{D/F}\n"
		return Response(E(),mimetype='text/plain')
	@route(f"{LAUNCHPAD_PATH}/metadata",methods=['GET'])
	def launchpad_metadata(self,request):
		try:C=unquote_and_validate_url(request)
		except werkzeug.exceptions.HTTPException as A:return Response(A.description,A.code)
		B=self.pods_cache.get_cached_pod_path(C);LOG.debug("Reading Pod's content from cached path %s",B);return Response(response=json.dumps(read_metadata_from_pod(B)),content_type='application/json')
	@route(f"{LAUNCHPAD_PATH}/inject",methods=['POST'])
	def launchpad_inject(self,request):
		try:C=unquote_and_validate_url(request)
		except werkzeug.exceptions.HTTPException as A:return Response(A.description,A.code)
		B=self.pods_cache.get_cached_pod_path(C);LOG.debug("Loading Pod's content from cached path %s",B);D=load_file(B,mode='rb');E=inject_pod_endpoint(content=D)
		if not E:return Response('Load failed',status=500)
def unquote_and_validate_url(request):
	A=request.values.get('url')
	if not A:raise BadRequest(description='Missing url as a query string parameter')
	try:A=urllib.parse.unquote(A);requests.head(A)
	except Exception:raise InternalServerError(description=f"Can't reach the specified URL: {A}")
	return A