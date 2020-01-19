import cups
conn = cups.Connection ()
printers = conn.getPrinters ()
f=open("test.txt","w")
f.write("TEST")
f.close()
f=open("test.txt","r")
for printer in printers:
    print(printer, printers[printer]["device-uri"])
    #printer_name=printers.keys().keys()
    print("########")
    #print(printer_name)
a=conn.printFile("LBP251","test.txt","Python_Status_print",{})
print(a)
