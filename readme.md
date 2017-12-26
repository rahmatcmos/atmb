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

## Instalasi OS
1. Download OS untuk raspberry pi (raspbian) di link berikut: http://vx2-downloads.raspberrypi.org/raspbian/images/raspbian-2017-08-17/2017-08-16-raspbian-stretch.zip

2. Ikuti langkah pada link berikut untuk instalasi OS pada SD card: https://www.raspberrypi.org/documentation/installation/installing-images/README.md

## Enable SSH
Masukkan SD Card yang telah terinstall OS Raspbian ke Laptop. Tambahkan baris ```/etc/init.d/ssh start``` pada file ```/etc/rc.local``` sebelum baris ```exit 0```. Edit file sebagai root

Kemudian setting IP Address dengan mengdit file sbb:

```
vim /etc/dhcpcd.conf
```

tambahkan baris berikut:

```
interface eth0
static ip_address=[IP Address]/[Subnet Mask]
static routers=[Default Gateway]
static domain_name_servers=[DNS Server]
```

## Setting raspbian
1. Koneksikan raspberry pi ke keyboard, mouse dan monitor
2. Buka terminal, check link below: https://www.raspberrypi.org/documentation/configuration/raspi-config.md

    Parameter yang perlu di setting:
    - Expand file system
    - Interface yg harus dienablekan = SPI, SSH, Serial
    - Booting GUI with user pi
    - Timezone
    - Locale
    - Overclock to turbo (if available)

## Setting Timezone

```
$ sudo dpkg-reconfigure tzdata
```

Pilih sesuai area setempat

## Package Dependency

Koneksi internet sementara bisa tathering via USB

```
$ sudo apt install vim python-pysqlite2 python-texttable python-qt4 python-qt4-phonon python-psutil sqlite3 wvdial ppp
$ sudo pip install terminaltables
$ sudo pip install pygame
```

## Installation

Login as ```pi``` user

```
$ cd ~
$ git clone https://github.com/udibagas/atmb.git ATMB
$ cd ATMB
$ chmod +x run.sh
```

Sesuaikan config

```
$ vim config.json
```

Parameter yang harus disesuaikan yaitu:

- id
- kode_kecamatan
- kode_kelurahan

## Pin Assignment

### Raspberry Pi

PIN | Type | Assignment | Koneksi
-- | -- | -- | --
16 | OUTPUT | Relay Motor ON | Pin INPUT relay 1 channel
18 | OUTPUT | Relay Arah Motor | Pin INPUT relay 2 channel (2 input digabung jadi 1)
22 | INPUT | Status Pintu | Sensor Magnet

## Setting USB port supaya fixed

Posisi | Nama | Koneksi
-- | -- | --
Kiri atas | serial2 | -
Kiri bawah | serial3 | -
Kanan atas | serial4 | -
Kanan bawah | serial5 | NFC

```
$ sudo mv 98-usb-serial.rules /etc/udev/rules.d/
$ sudo /etc/init.d/udev restart
```

Unplug, kemudian plug in NFC reader

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
Tambahkan baris berikut di paling bawah
```
@/usr/bin/python /home/pi/ATMB/atmb.py run
```

## Update saldo bulanan
Penerima menerima bantuan 15 liter tiap bulan.

```
$ crontab -e
```

Bagian paling bawah tambahkan baris berikut

```
@monthly sqlite3 /home/pi/ATMB/atmb.db 'update penerima set saldo = saldo + 15'
```

## CLI

```
$ killall python
$ cd ~/ATMB
$ python atmb.py
```

Akan muncul prompt sbb:

```
atmb>
```

Ketik ```?``` untuk melihat daftar perintah yang tersedia

### Mendaftarkan penerima
```
atmb> daftar
Nama : [masukkan nama kemudian enter]
[tempelkan kartu pada NFC reader]
```

Contoh output:
TODO

### Melihat list penerima
```
atmb> list
```

Contoh output:
TODO

### Melihat Log
```
atmb> log
```

Contoh output:
TODO

### Simulasi
Simulasi pengambilan beras
```
atmb> simulasi
```

### Test motor

Test motor maju/mundur dengan durasi sesuai config.json

#### Maju
```
atmb> motor push
```

Tekan ```Ctrl + C``` untuk cancel (motor akan berhenti)

#### Mundur
```
atmb> motor pull
```

Tekan ```Ctrl + C``` untuk cancel (motor akan berhenti)

### Test keypad

```
atmb> test keypad
```

Kemudian pencet tombol keypad dan pastian output sesuai.

### Test nfc
Untuk mengetest apakah kartu sudah terdaftar atau belum
```
atmb> test nfc
```

## Koneksi ke Server Menggunakan USB Modem

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

## Daftar Setting GSM

#### Telkomsel
```
Phone = *99#
Username = wap
Password = wap123
```

#### XL
```
Phone = *99#
Username: xlgprs
Password: proxl
```

#### Indosat
```
Phone = *99#
1. Time-besed
Username = indosat@durasi
Password = indosat@durasi
2. Volume-besed
Username = indosat
Password = indosat
```

#### Axis
```
Phone = *99#
Username: axis
Password: 123456
```

#### 3
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

## Menambah volume

```
$ amixer  sset PCM,0 90%
```
