# ATM BERAS

## Hardware
- Raspebrry Pi 3
- Micro SD 16GB class 10 (SanDisk)
- NFC (PN532)
- USB to Serial adapter
- Matrix Keypad
- Monitor 17 inch
- Kabel HDMI
- Power Supply Raspberry Pi (5V 2A)
- Power Supply Piston (24V 3A)
- Steker (3 terminal)
- Stop Kontak
- Relay (3)

## Software
- Raspbian (latest)
- Python

## Biar layar ga ngeblank (disable power saving mode)

```
$ sudo vim /etc/lightdm/lightdm.conf
```

ke line 87. Ubah sbb:

```
xserver-command=X -s 0 dpms
```

## Jalankan program setelah booting secara otomatis

```
$ vim ~/.config/lxsession/LXDE-pi/autostart
```
Tambahkan baris berikut
```
@/usr/bin/python /home/pi/ATMB/main-3l.py run
```

## Update saldo bulanan
Warga miskin menerima bantuan sebesar 15 liter per bulan.

```
$ crontab -e
```
Tambahkan baris berikut
```
@monthly mysql -u[user] -p[password] atmb -e "update nasabah set saldo = 15"
```
