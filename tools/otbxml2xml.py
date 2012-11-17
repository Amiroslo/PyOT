#!/usr/bin/env python
# -*- coding: latin-1 -*-

import struct, sys, io
from xml.dom.minidom import parse
import copy

# The reader class:
class Reader(object):
    def __init__(self, data):
        self.length = len(data)
        self.pos = 0
        self.data = data

    # 8bit - 1byte, C type: char
    def uint8(self):
        self.pos += 1
        return ord(self.data[self.pos-1])
        
    def peekUint8(self):
        try:
            return ord(self.data[self.pos])
        except:
            return None
    def int8(self):
        self.pos += 1
        return struct.unpack("<b", self.data[self.pos-1:self.pos])[0]

    # 16bit - 2bytes, C type: short
    def uint16(self):
        self.pos += 2
        return struct.unpack("<H", self.data[self.pos-2:self.pos])[0]
    def int16(self):
        self.pos += 2
        return struct.unpack("<h", self.data[self.pos-2:self.pos])[0]

    # 32bit - 4bytes, C type: int
    def uint32(self):
        self.pos += 4
        return struct.unpack("<I", self.data[self.pos-4:self.pos])[0]
    def int32(self):
        self.pos += 4
        return struct.unpack("<i", self.data[self.pos-4:self.pos])[0]

    # 64bit - 8bytes, C type: long long
    def uint64(self):
        self.pos += 8
        return struct.unpack("<Q", self.data[self.pos-8:self.pos])[0]
    def int64(self):
        self.pos += 8
        return struct.unpack("<q", self.data[self.pos-8:self.pos])[0]

    # 32bit - 4bytes, C type: float
    def float(self):
        self.pos += 4
        return struct.unpack("<f", self.data[self.pos-4:self.pos])[0]

    # 64bit - 8bytes, C type: double
    def double(self):
        self.pos += 8
        return struct.unpack("<d", self.data[self.pos-8:self.pos])[0]

    def string(self):
        length = self.uint16()
        self.pos += length
        return ''.join(map(str, struct.unpack("%ds" % length, self.data[self.pos-length:self.pos])))

    def getX(self, size):
        self.pos += size
        return ''.join(map(str, struct.unpack_from("B"*size, self.data, self.pos - size)))

    def getXString(self, size):
        self.pos += size
        return ''.join(map(str, struct.unpack("%ds" % size, self.data[self.pos-size:self.pos])))
        
    def getData(self):
        return self.data[self.pos:]
    
class Item(object):
    def __init__(self):
        self.type = 0
        self.flags = 0
        self.attr = {}
        self.cid = 0
        self.sid = 0
        self.alsoKnownAs = []
        self.junk = False

class Node(object):
    def __init__(self, otb):
        global LEVEL
        self.data = b""
        self.nodes = []
        byte = otb.uint8()
        nextIsEscaped = False
        while byte != None:
            if byte == 0xFE and not nextIsEscaped:
                node = self.handleBlock(otb)

            elif byte == 0xFF and not nextIsEscaped:
                LEVEL -= 1
                if LEVEL < 0:
                    print "DEBUG!"
                break
                
            elif byte == 0xFD and not nextIsEscaped:
                nextIsEscaped = True
                
            else:
                nextIsEscaped = False 
                self.data += struct.pack("<B", byte)
                
            byte = otb.uint8()
        self.data = Reader(self.data)
    def handleBlock(self, otb):
        global LEVEL
        LEVEL += 1
        node = Node(otb)
        self.nodes.append(node)
        return node
        
    def next(self):
        if self.nodes:
            return self.nodes.pop(0)
        else:
            return None
            
otbFile = io.open("items.otb", 'rb')
otb = Reader(otbFile.read())

otb.pos += 5
LEVEL = 1
node = Node(otb) # We use 1 here since we skip the "root"

node.data.uint8() # 0x00
node.data.uint32() # 0x00
node.data.uint8() # 0x01
node.data.uint16() # Really unimportant
majorVersion = node.data.uint32()
minorVersion = node.data.uint32()
buildVersion = node.data.uint32()
stringVersion = node.data.getXString(128)

print "-- "
print "-- OTB version %d.%d (Client: %s, build: %d)" % (majorVersion, minorVersion, stringVersion[12:16], buildVersion)

items = {}
lastRealItem = None

child = node.next()
while child:
    item = Item()
    item.type = child.data.uint8()
    item.flags = child.data.uint32()

    # FIX: It doesn't make sense to have walkstack on solid tiles...
    """if item.flags >= (1<<25) and item.flags & 1 and item.flags & (1<<25):
        item.flags -= 1 << 25"""

    # Actually, stackability are script based. And guess what, they got a "walkstack items.xml feature!". Ignore this "9.7" feature.
    if item.flags >= (1 << 25):
        item.flags -= 1 << 25
    if item.flags == 3:
        item.flags = "b" # block item.
    if item.flags == 1:
        item.flags = "s" # Solid item.
    if item.flags == 64:
        item.flags = "m" # Moveable.
    if item.flags == 96:
        item.flags = "p" # They hang (pickable + movable) tightly togetter hehe.
    if item.flags == 8192:
        item.flags = "t" # Top item.
    if item.flags == 8193:
        item.flags = "ts" # Top solid.
    if item.flags == 8195:
        item.flags = "tb" # Top block item.
    sub = child.next()
    while child.data.peekUint8():
        attr = child.data.uint8()
        datalen = child.data.uint16()
        if attr is 0x10:
            item.sid = child.data.uint16()
                    
        elif attr is 0x11:
            item.cid = child.data.uint16()
        elif attr == 0x12:
            item.attr["name"] = child.data.getXString(datalen)

        elif attr is 0x14:
            item.attr["speed"] = child.data.uint16()
            
        elif attr is 0x2B:
            item.attr["order"] = child.data.uint8()

        elif attr == 0x2C:
            item.attr["wareid"] = child.data.uint16()            
        else:
            child.data.pos += datalen        

    if item.cid:
        items[item.sid] = item
        lastRealItem = item
    else:
        lastRealItem.alsoKnownAs.append(item.sid)
        #items[item.sid] = lastRealItem
    child = node.next()
print "-- Got a total of %d items!" % len(items)
print "-- "
print ""

# Changes:
# * id and fromid-toid means clientId, not server id (as per kill-sid).
# * <attribute key= becomes <key>value</key> (shorter)

if __name__ == "__main__":
    import xml.etree.cElementTree as ET

    def topId(element):
        return int(element.get("id").split('-')[0])

    tree = ET.parse("items.xml")
    root = tree.getroot()
    index = 0
    ids = set()
    for item in root.findall("item"):
        # Kill some data we don't use.
        try:
            del item.attrib["article"]
        except:
            pass

        try:
            del item.attrib["plural"]
        except:
            pass

        if len(item):
            # Sub attributes.
            for attribute in item:
                key = attribute.get("key")
                if not key: continue
                val = attribute.get("value")

                if key in ("field",):
                    fields = {}
                    for attr in attribute:
                        elm = ET.Element("field" + attr.get("key").capitalize())
                        elm.set("value", attr.get("value"))
                        item.append(elm)
                        attr.clear()

                    attribute.clear()
                    attribute.set("value", val)

                if key in ("plural", "article", "cache", "blockprojectile", "type", "ammoAction", "forceSerialize"):
                    attribute.clear()
                    #item.remove(attribute)
                    continue # We auto generate those.
                if key in ("rotateTo", "decayTo", "transformEquipTo", "transformDeEquipTo", "transformUseTo") and int(val) != 0:
                    attribute.set("value", str(items[int(val)].cid))

                try:
                    del attribute.attrib["key"]
                except:
                    pass # Fields are reset so...
                attribute.tag = key
                
        id = int(item.get("id").split("-")[0]) if item.get("id") else int(item.get("fromid"))
        if id > 20000 and id < 20050: #or id not in items:
            item.clear()
            root.remove(item)
            continue

        #item.set("id", str(items[id].cid))
        #ids.add(items[id].cid)

        if items[id].type and items[id].type > 2: # I don't think we care for type 0 or type 1 or type 2 (aga containe$
            item.set("type", str(items[id].type))
        if "speed" in items[id].attr and items[id].attr["speed"] > 0 and items[id].attr["speed"] != 100:
            item.set("speed", str(items[id].attr["speed"]))
        if items[id].flags:
            item.set("flags", str(items[id].flags))

        if ("fromid" in item.attrib and "toid" in item.attrib and item.get("fromid") != item.get("toid")) or "-" in item.get("id", ""):
            if "-" in item.get("id", ""):
                orgId, toId = item.get("id").split("-")
                orgId = int(orgId)
                toId = int(toId)
            else:
                orgId = int(item.attrib["fromid"])
                toId = int(item.attrib["toid"])
                del item.attrib["fromid"]
                del item.attrib["toid"]
                item.set("id", "%s-%s" % (orgId, toId))
            i = 1
            if toId - orgId > 100:
                print "I think an item going from %d to %d is wrong...." % (orgId, toId)

            #item.set("id", str(orgId))
            ok = True
            orgFlags = items[orgId].flags
            orgCid = items[orgId].cid

            # First check that name, cid (incremental) & flags is the same.
            for id in xrange(orgId+1, toId+1):
                if items[id].flags != orgFlags or items[id].cid != orgCid + (id - orgCid):
                    ok = False

            # If not, unroll it.
            if not ok:
                for id in xrange(orgId+1, toId+1):
                    # Split items.
                    newItem = copy.deepcopy(item)
                
                    newItem.set("id", str(id))
                    root.insert(index+1, newItem)
                    
                    index += 1
                item.set("id", str(orgId))
                    
        elif "fromid" in item.attrib:
            # No toid. Rewrite.
            orgId = item.attrib["fromid"]
            del item.attrib["fromid"]
            item.set("id", orgId)

        index += 1

    # Rewrite ids.
    for item in root.findall("item"):
        # First some name checking.
        if "name" in items[topId(item)].attr and items[topId(item)].attr["name"] != item.get("name"):
            print (u"WARNING: Rewritting name of %s from %s to %s" % (item.get("id"), item.get("name"), items[topId(item)].attr["name"].decode('utf-8')))
            item.set("name", items[topId(item)].attr["name"].decode('utf-8'))

        flags = items[topId(item)].flags
        if flags:
            item.set("flags", str(flags))

        id = item.get("id")
        if "-" in id:
            start, end = map(int, id.split('-'))
            item.set("id", "%s-%s" % (items[start].cid, items[end].cid))
            for id in xrange(items[start].cid, items[end].cid+1):
                ids.add(id)
        else:
            id = items[int(item.get("id"))].cid
            item.set("id", str(id))
            if id in ids:
                print "WARNING: ItemId %d got two entries!" % (id)
                if not len(item):
                    root.remove(item)
            ids.add(id)

    for item in items.values():
        if item.cid not in ids:
            elm = ET.Element('item')
            elm.set('id', str(item.cid))
            if item.flags:
                elm.set('flags', str(item.flags))
            if item.type and item.type > 2:
                elm.set('type', str(item.type))
            if "speed" in item.attr and item.attr["speed"] > 0 and item.attr["speed"] != 100:
                elm.set('speed', str(item.attr["speed"]))
            if "name" in item.attr:
                elm.set('name', item.attr["name"].decode('utf-8'))

            ids.add(item.cid)

            root.append(elm)

    # Sort it.
    container = root.findall("item")
    data = []
    for elem in container:
        key = topId(elem)
        data.append((key, elem))

    data.sort()

    # insert the last item from each tuple
    container[:] = [item[-1] for item in data]

    # Reapply ranges.
    currElem = None
    currId = 0
    cuFlags = None
    currName = ""
    count = 0
    i = 0
    for elem in container:
        id = elem.get("id")
        if "-" in id: continue
        
        id = int(id)
        if id == currId + count + 1 and currName == elem.get("name") and currFlags == elem.get("flags"):
            count += 1
            root.remove(elem)
            continue
        elif count:
            currElem.set("id", "%s-%s" % (currId, currId+count))

        currElem = elem
        currId = id
        currFlags = elem.get("flags")
        currName = elem.get("name")
        count = 0
                
    tree.write("out.xml")
 
    data = parse("out.xml").toprettyxml(encoding="utf-8", newl="\n")
    with open("out.xml", 'w') as f:
        data = data.replace("\t\t<attribute/>\n", "\t")
        data = data.replace("\t\t\n\t\t\n", "").replace("\t\n\t\n", "\n").replace("\">\n\t\t</item>\n", "\"/>\n")
        data = data.replace("/>\n\n", "/>\n").replace("\n\t\n", "\n")
        data = data.replace("\t\t\t</item>", "\t</item>").replace("\t\t</item>", "\t</item>")
        data = data.replace("\t\t\t", "\t\t").replace("\t\t\t", "\t\t") # We do this twice.
        f.write(data)

        