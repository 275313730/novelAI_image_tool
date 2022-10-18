import os
import json
import imageio.v3 as iio


def get_images_data():
    print('**程序运行中**')
    with open('./config.json', 'r', encoding='utf8') as fp:
        print('-正在打开config.json')
        config = json.load(fp)
        images_dir = config["images_dir"]
        images_data = []
        print('-正在获取图片列表')

        error_files = []
        for root, dirs, files in os.walk(config['images_dir']):
            print('-正在分析图片数据')
            for file in files:
                if "png" not in file:
                    error_files.append(file)
                    continue
                metadata = iio.immeta('./' + images_dir + "/" + file)

                if not metadata:
                    error_files.append(file)
                    continue

                keywords_array = metadata['Description'].split(',')
                for index in range(len(keywords_array)):
                    keywords_array[index] = keywords_array[index].lstrip().rstrip().replace('\u00a0', ' ')

                comment = json.loads(metadata['Comment'])
                negative_keywords_array = comment['uc'].split(',')
                for index in range(len(negative_keywords_array)):
                    negative_keywords_array[index] = negative_keywords_array[index].lstrip().rstrip().replace('\u00a0',
                                                                                                              ' ')

                image_url = "./images/" + images_dir + "/" + file
                image_data = {"keywordsArray": keywords_array,
                              "negativeKeywordsArray": [],
                              "imageUrl": image_url,
                              "steps": comment['steps'],
                              "strength": comment['strength'],
                              "noise": comment['noise'],
                              "scale": comment['scale'],
                              "seed": comment['seed'],
                              "sampler": comment['sampler'],
                              'r18': config['r18']}
                images_data.append(image_data)
        print('-图片数据分析完成')

        json_path = "./" + images_dir + ".json"
        f = open(json_path, 'w')
        f.write(json.dumps(images_data))
        f.close()
        print('-文件' + images_dir + ".json已生成")
        if len(error_files) > 0:
            print('-无效文件如下:' + str(error_files))
        print('**处理完成**')

    os.system('pause')


get_images_data()
