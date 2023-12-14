from multiprocessing import Pool
from PIL import Image
import keyboard
import requests
import sys
import io

'''
Before Using the script you need to get the links from scribd

1: Use autoscroller to get all the urls of the images. 
2: Copy the HAR response
3: Open the chrome console and create a var har = [Paste it here]
4: Run the following snipit 

var imageUrls = [];
har.log.entries.forEach(function (entry) {
  // This step will filter out all URLs except images. If you just want e.g. just jpg's then check mimeType against "image/jpeg", etc.
  if (entry.response.content.mimeType.indexOf("image/") !== 0) return;
  imageUrls.push(entry.request.url);
});
console.log(imageUrls.join('\n'));

Copy the response and delete the links that you dont need 
Run the script no arguments needed, if its a page other than Scribd, edit the url trimming and,
make sure the images are pasted in the right order 
'''

def toPDF(result):
    image_list = list(result)
    image_list[0].save(r'yoink.pdf', save_all=True, append_images=image_list, quality=100, subsampling=0)
    print("Done : )", flush=True)

def imgDownloader(arg):
    try:
        url =  arg[0]
        n = url.find("-")
        number = url[54:n]
        img_data = requests.get(url).content
        image = Image.open(io.BytesIO(img_data))
        print(number+" Downloaded", flush=True)
        return (image)
        
    except(Exception) as e:
        print("lole",e,flush=True) 
   
if __name__ == '__main__':
    URLs = []
    with open("links.txt", "r") as file:
            for line in file:
                URLs.append(line.rstrip())
            else:
                print("Links Loaded", flush=True)
    for i in range(len(URLs)):
        URLs[i]= [URLs[i],1]
    with Pool(6) as pool:
        result = pool.map_async(imgDownloader,URLs,callback=toPDF)
        keyboard.wait("esc")
        print("bye")
        sys.exit()

