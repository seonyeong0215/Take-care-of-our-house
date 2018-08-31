import cls_singleton

#cls1 = cls_singleton.Cls()
cls1 = cls_singleton.MyCls.instance()
cls2 = cls_singleton.MyCls.instance()

vals1 = cls1.getValue()
vals2 = cls2.getValue()

print(str(vals1['temp']) + "," + str(vals1['bpm']))
print(str(vals1['temp']) + "," + str(vals1['bpm']))

cls1.addValue()

print(str(vals1['temp']) + "," + str(vals1['bpm']))
print(str(vals2['temp']) + "," + str(vals2['bpm']))

cls3 = cls_singleton.MyCls.instance()
vals3 = cls3.getValue()

print(str(vals3['temp']) + "," + str(vals3['bpm']))