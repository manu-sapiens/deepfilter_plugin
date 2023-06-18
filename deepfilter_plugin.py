# --------------- SHARED ---------------------------------------------------
import sys
from typing import List, Any
sys.path.append('.')  # Add the current directory to the sys path
sys.path.append('utils')  # Add the utils directory to the sys path

from utils.omni_utils_http import CdnResponse, ImageMeta, create_api_route, plugin_main, init_plugin
from pydantic import BaseModel
app, router = init_plugin()
# ---------------------------------------------------------------------------
plugin_module_name="Plugins.deepfilter_plugin.deepfilter"

# --------------- DEEPFILTER ENHANCE ----------------------------
ENDPOINT_DEEPFILTER_ENHANCE = "/deepfilter/enhance"

class DeepfilterEnhance_Input(BaseModel):

    audio: List[CdnResponse]
    
    class Config:
        schema_extra = {
            "title": "deepfilter: enhance"
        }

class DeepfilterEnhance_Response(BaseModel):
    media_array: List[CdnResponse]
 
    class Config:
        schema_extra = {
            "title": "deepfilter: enhance"
        }
 
DeepfilterEnhance_Post = create_api_route(
    app=app,
    router=router,
    context=__name__,
    endpoint=ENDPOINT_DEEPFILTER_ENHANCE,
    input_class=DeepfilterEnhance_Input,
    response_class=DeepfilterEnhance_Response,
    handle_post_function="integration_DeepfilterEnhance_Post",
    plugin_module_name=plugin_module_name
)

endpoints = [ENDPOINT_DEEPFILTER_ENHANCE]

# --------------- SHARED ---------------------------------------------------
plugin_main(app, __name__, __file__)
# --------------------------------------------------------------------------