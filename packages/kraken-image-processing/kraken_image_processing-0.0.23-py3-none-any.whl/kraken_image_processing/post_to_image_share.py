import asyncio
import aiohttp
import pyimgbox
from kraken_image_processing.extractors import kraken_image_hash 
import cv2



def post(input_records = None):
    """Takes schema record entity and load image from path defined at temp:filepath
    Returns new imageobject with contenturl and thumbnailurl
    """

    #loop = asyncio.get_event_loop()
    #loop = asyncio.new_event_loop()
    
    #output_records = loop.run_until_complete(post_async(input_records))

    output_records = asyncio.run(post_async(input_records))
    
    return output_records

async def post_async(input_records):
    """Takes schema record entity and load image from path defined at temp:filepath
    Returns new imageobject with contenturl and thumbnailurl
    """

    if not isinstance(input_records, list): 
        input_records = [input_records]

    # Write files to site
    tasks = []
    tasks.append(asyncio.ensure_future(post_to_image_sharing(input_records)))
    output_records = await asyncio.gather(*tasks, return_exceptions=True)
    
    return output_records


async def post_to_image_sharing(input_records):

    # Get filepaths from records
    filepaths = []
    for r in input_records:
        
        img = r.get('temp:cv2_img', None)
        img_pil = r.get('temp:pil_img', None)
        hash = kraken_image_hash.get(img) 
        
        folder = 'temp'
        extension = 'jpg'
        name = folder + '/' + hash + '.' + extension

        img_pil.save(name)
        filepaths.append(name)
        r['temp:filepath'] = name
        
        

    # Load filepaths
    output_records = []
    async with pyimgbox.Gallery(title="References", adult = True, square_thumbs = True, thumb_width = 200) as gallery:
        try:
            async for submission in gallery.add(filepaths):

                #print(submission)
                record_imageObject = {
                    '@type': 'schema:ImageObject',
                    'schema:thumbnailUrl': submission.thumbnail_url,
                    'schema:contentUrl': submission.image_url
                }
                
                # Find corresponding record id
                for i in input_records:
                    if i.get('temp:filepath', None) == submission.filepath:
                        record_imageObject['@id'] = i.get('@id', None)

                
                output_records.append(record_imageObject)
                
        except Exception as e:
            print('error', e)
    

    
    return output_records

post()

