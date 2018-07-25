/*
 * =========================================================================================
 * Name        : GraphColoringBestFirstSearch
 * Author      : Anh Minh Phuc Nguyen
 * Email       : panguyen5297@gmail.com
 * Description : This file implement a solution for Vietnam Map Graph Coloring using Best
 *               First Search algorithm.
 * =========================================================================================
 */

import random
import time
import queue
import copy

VIETNAM_GRAPH = {
    'LaiChau' :['LaoCai','DienBien','SonLa','YenBai'],
    'DienBien' :['LaiChau','SonLa'],
    'LaoCai' :['YenBai','HaGiang','LaiChau'],
    'HaGiang' :['LaoCai','YenBai','TuyenQuang','CaoBang'],
    'CaoBang' :['HaGiang','BacKan','LangSon'],
    'SonLa' :['DienBien','LaiChau','YenBai','PhuTho','HoaBinh','ThanhHoa'],
    'YenBai' :['SonLa','LaiChau','LaoCai','HaGiang','TuyenQuang','PhuTho'],
    'TuyenQuang' :['YenBai','HaGiang','BacKan','ThaiNguyen','VinhPhuc','PhuTho'],
    'BacKan':['TuyenQuang','CaoBang','LangSon','ThaiNguyen'],
    'PhuTho':['SonLa','YenBai','TuyenQuang','VinhPhuc','HaNoi','HoaBinh'],
    'VinhPhuc':['PhuTho','TuyenQuang','ThaiNguyen','HaNoi'],
    'ThaiNguyen':['VinhPhuc','TuyenQuang','BacKan','LangSon','BacGiang','HaNoi'],
    'LangSon':['ThaiNguyen','BacKan','CaoBang','BacGiang','QuangNinh'],
    'HoaBinh':['SonLa','PhuTho','HaNoi','HaNam','NinhBinh','ThanhHoa'],
    'HaNoi':['HoaBinh','PhuTho','VinhPhuc','ThaiNguyen','BacGiang','BacNinh','HungYen','HaNam'],
    'BacGiang':['HaNoi','ThaiNguyen','LangSon','QuangNinh','HaiDuong','BacNinh'],
    'QuangNinh':['HaiPhong','HaiDuong','BacGiang','LangSon'],
    'NinhBinh':['ThanhHoa','HoaBinh','HaNam','NamDinh'],
    'HaNam':['NinhBinh','HoaBinh','HaNoi','HungYen','ThaiBinh','NamDinh'],
    'HungYen':['HaNam','HaNoi','BacNinh','HaiDuong','ThaiBinh'],
    'BacNinh':['HungYen','HaNoi','BacGiang','HaiDuong'],
    'HaiDuong':['HungYen','BacNinh','BacGiang','QuangNinh','HaiPhong','ThaiBinh'],
    'NamDinh':['NinhBinh','HaNam','ThaiBinh'],
    'ThaiBinh':['NamDinh','HaNam','HungYen','HaiDuong','HaiPhong'],
    'HaiPhong':['ThaiBinh','HaiDuong','QuangNinh'],
    'ThanhHoa':['HoaBinh','NinhBinh','NgheAn','SonLa'],
    'NgheAn':['ThanhHoa','HaTinh'],
    'HaTinh':['NgheAn','QuangBinh'],
    'QuangBinh':['HaTinh','QuangTri'],
    'QuangTri':['QuangBinh','ThuaThienHue'],
    'ThuaThienHue':['QuangTri','DaNang','QuangNam'],
    'DaNang':['ThuaThienHue','QuangNam'],
    'QuangNam':['ThuaThienHue','DaNang','QuangNgai','KonTum'],
    'KonTum':['QuangNam','QuangNgai','GiaLai'],
    'QuangNgai':['KonTum','QuangNam','BinhDinh'],
    'GiaLai':['KonTum','BinhDinh','PhuYen','DakLak'],
    'BinhDinh':['GiaLai','QuangNgai','PhuYen'],
    'PhuYen':['GiaLai','BinhDinh','DakLak','KhanhHoa'],
    'DakLak':['GiaLai','PhuYen','KhanhHoa','LamDong','DakNong'],
    'KhanhHoa':['DakLak','PhuYen','NinhThuan','LamDong'],
    'DakNong':['DakLak','LamDong','BinhPhuoc'],
    'LamDong':['DakNong','DakLak','KhanhHoa','NinhThuan','BinhThuan','DongNai','BinhPhuoc'],
    'NinhThuan':['LamDong','KhanhHoa','BinhThuan'],
    'TayNinh':['BinhPhuoc','BinhDuong','TPHCM','LongAn'],
    'BinhDuong':['TayNinh','BinhPhuoc','DongNai','TPHCM'],
    'DongNai':['BinhDuong','BinhPhuoc','LamDong','BinhThuan','BaRiaVungTau','TPHCM'],
    'BinhPhuoc':['TayNinh', 'BinhDuong','DongNai','LamDong','DakNong'],
    'BinhThuan':['BaRiaVungTau','DongNai','LamDong','NinhThuan'],
    'LongAn':['DongThap','TienGiang','TPHCM','TayNinh'],
    'TPHCM':['LongAn','TayNinh','BinhDuong','DongNai'],
    'BaRiaVungTau':['DongNai','BinhThuan'],
    'DongThap':['AnGiang','LongAn','TienGiang','VinhLong','CanTho'],
    'TienGiang':['DongThap','LongAn','BenTre','VinhLong'],
    'AnGiang':['KienGiang','DongThap','CanTho'],
    'CanTho':['KienGiang','AnGiang','DongThap','VinhLong','HauGiang'],
    'VinhLong':['CanTho','DongThap','TienGiang','BenTre','TraVinh','HauGiang'],
    'BenTre':['TienGiang','TraVinh','VinhLong'],
    'KienGiang':['AnGiang','CanTho','HauGiang','BacLieu','CaMau'],
    'HauGiang':['KienGiang','CanTho','VinhLong','SocTrang','BacLieu'],
    'TraVinh':['SocTrang','VinhLong','BenTre'],
    'CaMau':['KienGiang','BacLieu'],
    'BacLieu':['CaMau','KienGiang','HauGiang','SocTrang'],
    'SocTrang':['BacLieu','HauGiang','TraVinh'],
}
COLOURS = ('red', 'yellow', 'blue', 'green', 'purple', 'black', 'white', 'gray', 'pink', 'orange')

def findGraphColor(graph, colorNumber):

    # Variables initiate
    startTime = time.time()
    goalScore = 0
    colorList = []
    for i in range(0, int(colorNumber)):
        colorList.append(COLOURS[i])

    # Finding the goal score
    for node, adjacent in graph.items():
        goalScore -= len(adjacent)
    print("Goal Score:", goalScore)

    # provinces list and province's color list
    provinces = []
    colors = []

    # Initial State: Coloring the graph randomly
    for node in graph.keys():
        colors.append(random.choice(colorList))
        provinces.append(node)

    # Start Best First Search
    solution = BestFirstSearch(graph, colors, provinces, colorList, goalScore)

    # Display result
    print("FINISH")
    if solution == None:
        print("No Solution !!!")
    else:
        for index1 in range(0, len(provinces)):
            print("Province:", provinces[index1], "- Color:", solution[index1])
            for node, adjacents in graph.items():
                if node == provinces[index1]:
                    for index2 in range(0, len(adjacents)):
                        adjacentIndex = provinces.index(adjacents[index2])
                        print("Adjacent:", adjacents[index2], "-", solution[adjacentIndex])
                    break
            print("------------------------------------------------------")
    endTime = time.time()
    print("Elapsed time: ", endTime - startTime)

def BestFirstSearch(graph, colors, provinces, colorList, goalScore):

    # Variables initiate
    openList = queue.PriorityQueue()
    hasBorn = []
    index = 0

    # Insert the first element to priority queue
    openList.put(copy.deepcopy(colors), measureScore(graph, colors, provinces))
    hasBorn.append(copy.deepcopy(colors))

    # Loop until priority queue is empty or solution is found
    while (openList.empty() == False):

        currentState = openList.get()
        colors = copy.deepcopy(currentState)

        # Goal score checking
        currentScore = measureScore(graph, colors, provinces)
        if currentScore == goalScore:
            return colors

        # Choose the index to find successors
        checkJump = False
        for node, adjacents in graph.items():
            for i1 in range(0, len(adjacents)):
                index1 = provinces.index(node)
                index2 = provinces.index(adjacents[i1])
                if colors[index1] == colors[index2]:
                    index = index1
                    checkJump = True
                    break
            if checkJump:
                break

        print("Current score:", currentScore)

        # Find the successors and put them to priority queue
        for i in range(0, len(colorList)):
            colors[index] = colorList[i]
            localScore = measureScore(graph, colors, provinces)
            if colors not in hasBorn:
                openList.put(copy.deepcopy(colors), localScore)
                hasBorn.append(copy.deepcopy(colors))

    return None

# Heuristic Function
def measureScore(graph, colors, provinces):
    index1 = 0
    score = 0
    for node,adjacents in graph.items():
        for i in range(0,len(adjacents)):
            index2 = provinces.index(adjacents[i])
            if (colors[index2] == colors[index1]):
                score = score + 1
            else: score = score - 1
        index1 = index1 + 1
    return score

if __name__ == '__main__':
    graph = VIETNAM_GRAPH
    print("*********************************************")
    print("VIETNAM MAP COLORING USING BEST FIRST SEARCH")
    colorNumber = input("Type number of color you want to use (Maximum-10): ")
    while (int(colorNumber)<= 0 or int(colorNumber) > 10):
        colorNumber = input("Type number of color you want to use (Maximum-10): ")
    colors = findGraphColor(graph, colorNumber)
