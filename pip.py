from sys import argv
import shapely.geometry as g
import csv

## "00000" : {"0.00", "0.00"}
poly_map = {}
zone_map = {}

zone_zip = ""

#p1 = g.Point(20.987404, -89.591060)
#print(p1.within(poly_map['97145']))

def find_zip(p):
    for k, _ in poly_map.items():
        if p.within(poly_map[k]):
            return k
    return "no hay match"

def is_zone(p):
    return p.within(zone_map[zone_zip])
    


if __name__ == '__main__':
    ## parse csv data to zipode to point list
    with open('data.csv') as f:
        r = csv.reader(f, delimiter=";")
        for row in r:
            if len(row[1]) < 12:
                continue
            list_xys = row[1].split()
            list_xy_point = []
            for xy in list_xys:
                tmp = xy.split(",")
                if len(tmp) < 2:
                    continue
                list_xy_point.append(g.Point(float(tmp[1]), float(tmp[0]))) 
            poly_map[row[0]] = g.Polygon([[p.x, p.y] for p in list_xy_point])

    with open('zone.csv') as f:
        r = csv.reader(f, delimiter=";")
        for row in r:
            if len(row[1]) < 12:
                continue
            list_xys = row[1].split()
            list_xy_point = []
            for xy in list_xys:
                tmp = xy.split(",")
                if len(tmp) < 2:
                    continue
                list_xy_point.append(g.Point(float(tmp[1]), float(tmp[0]))) 
            zone_zip = row[0]
            zone_map[row[0]] = g.Polygon([[p.x, p.y] for p in list_xy_point])

    with open('in.csv', 'r') as r, open('out.csv', 'w') as w:
        rdr = csv.reader(r)
        wtr = csv.writer(w)
        for row in rdr:
            p = g.Point(float(row[1]), float(row[2]))

            row.append(find_zip(p))
            row.append(is_zone(p))

            wtr.writerow(row)
        

    # if len(argv) != 3:
    #     print("No. de argumentos incorrectos")
    #     print("python3 pip.py x y")
    #     exit(1)
    
    # p = g.Point(float(argv[1]), float(argv[2]))
    # print(find_zip(p))