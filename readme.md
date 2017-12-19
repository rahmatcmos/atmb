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

## Interkoneksi

- NFC : Port USB kanan bawah

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

### Koneksi ke server

```
$ sudo apt install wvdial
```

Koneksikan modem ke Raspberry Pi pada port USB kiri atas.

```
$ sudo wvdialconf
```

Edit ```/etc/wvdial.conf``` dibagian berikut:

```
Phone = *99#
Password = "wap123"
Username = "wap"
```

### Daftar Setting GSM

Telkomsel
```
Phone = *99#
Username = wap
Password = wap123
```

XL
```
Phone = *99#
Username: xlgprs
Password: proxl
```

Indosat
```
Phone = *99#
1. Time-besed
Username = indosat@durasi
Password = indosat@durasi
2. Volume-besed
Username = indosat
Password = indosat
```

Axis
```
Phone = *99#
Username: axis
Password: 123456
```

3
```
Phone = *99#
Username = 3data
Password = 3data
```

## Koneksi ke modem otomatis

Buat script untuk start modem

```
$ vim ~/start_modem.sh
```

Isi file sbb:

```
#!/bin/bash

sleep 30
sudo wvdial &
```

Buat agar script executable

```
$ chmod +x ~/start_modem.sh
```

```
$ vim ~/.config/lxsession/LXDE-pi/autostart
```

Bagian paling bawah tambahkan baris berikut

```
@/home/pi/start_modem.sh
```

## Otomatis menambahkan saldo saldo tiap bulan

```
$ sudo apt install sqlite3
$ crontab -e
```

Bagian paling bawah tambahkan baris berikut

```
@monthly sqlite3 /home/pi/ATMB/atmb.db 'update penerima set saldo = saldo + 15'
```
