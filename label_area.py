#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import os
import json
import shutil
import math
path = r'C:\Users\Jisoo\Desktop\label_area'# 작업경로
path2 = r'C:\Users\Jisoo\Desktop\label_area_error' # 에러폴더 보관 경로
global area_list
area_list = {}

                
def label_area(path, folder, file, jdata):
    json_path = path+'/'+folder+'/'+file
    jfile = open(json_path, 'rt', encoding = 'UTF8')
    jdata = json.load(jfile)
    jfile.close()
    bound_cnt = int(jdata['BoundingCount'])
    for k in range(0, bound_cnt):
        if jdata['Bounding'][k]['Drawing'] == 'BOX':
            x1 = int(jdata['Bounding'][k]['x1'])
            x2 = int(jdata['Bounding'][k]['x2'])
            y1 = int(jdata['Bounding'][k]['y1'])
            y2 = int(jdata['Bounding'][k]['y2'])
            area = (x2 - x1) * (y2 - y1)
        elif jdata['Bounding'][k]['Drawing'] == 'POLYGON':
            jfile = open(json_path, 'rt', encoding = 'UTF8')
            jdata = json.load(jfile)
            jfile.close()
            point_cnt = int(jdata['Bounding'][k]['PolygonCount'])
            n = point_cnt
            coord_list = []
            for i in range(point_cnt):
                a = list(jdata['Bounding'][k]['PolygonPoint'][i].values())
                x,y = int(a[0].split(',')[0]),int(a[0].split(',')[1])
                coord_list.append([x, y])

            coord_list.append(coord_list[0])
            plus = 0
            minus = 0
            for i in range(len(coord_list) - 1):
                plus += (coord_list[i][0] * coord_list[i+1][1])
                minus += (coord_list[i][1] * coord_list[i+1][0])
            area = math.fabs(0.5 * (plus - minus))
        if area < area_list[folder][1]:
            area_list[folder][0] = file
            area_list[folder][1] = area
        else:
            pass

cnt=0
for folder in os.listdir(path):
    cnt+=1
    if cnt%1000 ==0:
        print(cnt)
    for file in os.listdir(path+'/'+folder):
        if file.endswith('Json'):
            json_path = path+'/'+folder+'/'+file
            jfile = open(json_path, 'rt', encoding='UTF8')
            jdata = json.load(jfile)
            jfile.close()
            bound_cnt = int(jdata['BoundingCount'])
            try:
                if area_list[folder] != ['',999999999999]:
                    label_area(path, folder, file, jdata)
            except:
                area_list[folder] = ['',999999999999]
                label_area(path, folder, file, jdata)
                
cnt=0
for folder in os.listdir(path):
    cnt+=1
    if cnt%1000==0:
        print(cnt)
    f_list = [i for i in os.listdir(path+'/'+folder) if i.endswith('Json')]
    for file in os.listdir(path+'/'+folder):
        if file.endswith('Json'):
            if file in area_list[folder][0]:
                direction = '원거리'
                f_list.remove(file)
            elif file == f_list[0]:
                direction = '정면'
            else:
                direction = '측면'


            try:
                json_path = path+'/'+folder+'/'+file
                jfile = open(json_path, 'rt', encoding='UTF8')
                jdata = json.load(jfile)
                jfile.close()
                bound_cnt = int(jdata['BoundingCount'])
                new_jdata = {}
                new_jdata['FILE NAME'] = jdata['FILE NAME']
                new_jdata['COLLECTION METHOD'] =jdata['COLLECTION METHOD']
                new_jdata['FORM'] = jdata['FORM']
                new_jdata['DATE'] = jdata['DATE']
                new_jdata['GPS'] = jdata['GPS']
                new_jdata['ID CODE'] = jdata['ID CODE']
                new_jdata['RESOLUTION'] = jdata['RESOLUTION']
                new_jdata['focus distance'] = jdata['focus distance']
                new_jdata['exposure time'] = jdata['exposure time']
                new_jdata['Aperture values'] = jdata['Aperture values']
                new_jdata['Sensitivity iso'] = jdata['Sensitivity iso']
                new_jdata['exposure method'] = jdata['exposure method']
                new_jdata['MAKE'] = jdata['MAKE']
                new_jdata['Camera Model Name'] = jdata['Camera Model Name']
                new_jdata['Software'] = jdata['Software']
                new_jdata['File Size'] = jdata['File Size']
                new_jdata['DAY/NIGHT'] = jdata['DAY/NIGHT']
                new_jdata['PLACE'] = jdata['PLACE']
                new_jdata['PROJECT SORTING'] = jdata['PROJECT SORTING']
                new_jdata['BoundingCount'] = jdata['BoundingCount']
                new_jdata['Bounding'] = []
                for k in range(0, bound_cnt):
                    new_jdata['Bounding'].append({})
                    new_jdata['Bounding'][k]['CLASS'] = jdata['Bounding'][k]['CLASS']
                    new_jdata['Bounding'][k]['DETAILS'] = jdata['Bounding'][k]['DETAILS']
                    new_jdata['Bounding'][k]['DAMAGE'] = jdata['Bounding'][k]['DAMAGE']
                    new_jdata['Bounding'][k]['TRANSPARENCY'] = jdata['Bounding'][k]['TRANSPARENCY']
                    new_jdata['Bounding'][k]['Color'] = jdata['Bounding'][k]['Color']
                    new_jdata['Bounding'][k]['DETAILS'] = jdata['Bounding'][k]['DETAILS']
                    new_jdata['Bounding'][k]['Shape'] = jdata['Bounding'][k]['Shape']
                    if jdata['PROJECT SORTING'] == '산업폐기물':
                        new_jdata['Bounding'][k]['Material'] = jdata['Bounding'][k]['Material']
                    else:
                        new_jdata['Bounding'][k]['Texture'] = jdata['Bounding'][k]['Texture']
                    new_jdata['Bounding'][k]['Object Size'] = jdata['Bounding'][k]['Object Size']
                    new_jdata['Bounding'][k]['Direction'] = direction
                    new_jdata['Bounding'][k]['Drawing'] = jdata['Bounding'][k]['Drawing']
                    if new_jdata['Bounding'][k]['Drawing'] == 'BOX':
                        new_jdata['Bounding'][k]['x1'] = jdata['Bounding'][k]['x1']
                        new_jdata['Bounding'][k]['y1'] = jdata['Bounding'][k]['y1']
                        new_jdata['Bounding'][k]['x2'] = jdata['Bounding'][k]['x2']
                        new_jdata['Bounding'][k]['y2'] = jdata['Bounding'][k]['y2']
                    else:
                        new_jdata['Bounding'][k]['PolygonCount'] = jdata['Bounding'][k]['PolygonCount']
                        new_jdata['Bounding'][k]['PolygonPoint'] = jdata['Bounding'][k]['PolygonPoint']

                jfile = open(json_path, 'wt', encoding = 'UTF8')
                json.dump(new_jdata, jfile, indent = 2, ensure_ascii = False)
                jfile.close()
            except:
                print(json_path)
                try:
                    shutil.move(path+'/'+folder, path2+'/'+folder)
                except:
                    pass
                pass

