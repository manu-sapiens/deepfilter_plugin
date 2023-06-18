print("---------- Deepfilter Integration ----------------")
from utils.omni_utils_misc import omni_get_env
OMNI_TEMP_FOLDER = omni_get_env("OMNI_TEMP_FOLDER")

from utils.omni_utils_http import CdnHandler
from fastapi import HTTPException
import os
#-----------------------

from df.enhance import enhance, init_df, load_audio, save_audio

from Plugins.deepfilter_plugin.deepfilter_definitions import DeepfilterEnhance_Input, DeepfilterEnhance_Response

async def integration_DeepfilterEnhance_Post(input: DeepfilterEnhance_Input):
    cdn = CdnHandler()
    if True: #try:
        cdn.announcement()
        print("------------- deepfilter enhance ------------------")
        print(f"input = {input}")

        audios = input.audio
        print(f"audios = {audios}")
       
        enhanced_filenames = []
        if audios is not None and len(audios) >0:
            model, df_state, _ = init_df()  # Load default model

            input_cdns = audios 
            input_filenames = await cdn.download_files_from_cdn(input_cdns)
            for input_filename in input_filenames:
                noisy_audio, _ = load_audio(input_filename, sr=df_state.sr())
           
                enhanced_audio = enhance(model, df_state, noisy_audio)
                enhanced_filename = os.path.join(OMNI_TEMP_FOLDER, f"{input_filename}_enhanced.wav")
                save_audio(enhanced_filename, enhanced_audio, df_state.sr())
                enhanced_filenames.append(enhanced_filename)
            #

        results_cdns = []
        if len(enhanced_filenames) > 0:
            print(f"Uploading # {len(enhanced_filenames)}")
            results_cdns = await cdn.upload_files_to_cdn(enhanced_filenames)
            print(f"results_cdns = {results_cdns}")
            
            # delete the results files from the local storage
            cdn.delete_temp_files(enhanced_filenames)
        #

        print(f'Processed {input_filename} and found {len(enhanced_filenames) } segments')
        response = DeepfilterEnhance_Response(media_array=results_cdns)

        print("\n-----------------------\n")
        return response
    else: #except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
