#!/usr/bin/python

import binascii
import sys
import time
import PN532
import MySQLdb

db_con = MySQLdb.connect(host="localhost", user="root", passwd="bismillah", db="atmb")
pn532 = PN532.PN532("/dev/serial0", 115200)
pn532.begin()
pn532.SAM_configuration()

# Get the firmware version from the chip and print(it out.)
ic, ver, rev, support = pn532.get_firmware_version()
print('Waiting for MiFare card...')
while True:
    uid = pn532.read_passive_target()
    if uid is "no_card":
        continue
    card_id = str(binascii.hexlify(uid))

    cur = db_con.cursor()
    cur.execute("INSERT INTO nasabah (nama, saldo, pin, card_id, alamat) VALUES ('PENERIMA', 15, AES_ENCRYPT('1234', UNHEX('F3229A0B371ED2D9441B830D21A390C3')), AES_ENCRYPT(%s, UNHEX('F3229A0B371ED2D9441B830D21A390C3')), '-')",
                (card_id,))
    cur.close()
    db_con.commit()
    print "OK : " + card_id;
    time.sleep(2)