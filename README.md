## APK Patcher

This tool was developed mainly to automatically insert Frida Gadget inside APKs but helps also in other common tasks while reversing Android apps.

Frida Website: https://frida.re/

Frida Github: https://github.com/frida/frida


#### Features
- Automatically insert Frida gadget library in APK, so you can use Frida without root - [Reference](https://frida.re/docs/gadget/)
- Configure Frida Gadget to automatically load hooks javascript file, without requiring the use of Frida client
- Insert a network configuration in APK that allows the application to use User Certificate Authorities - [Reference](https://android-developers.googleblog.com/2016/07/changes-to-trusted-certificate.html)
- Help during the tedious tasks of decompiling, modify code, repackaging, resign, zipalign

#### How To Install
##### Dependencies
Starting with 1.2.0 only `java` is a required dependency, with `Frida` and `adb` as optional dependencies.

- java (optional and will be automatically installed if it doesn't exist)
- adb (optional to automatically detect target architecture)

##### Termux

 Termux has 2 extra dependencies.

 - custom apktool - https://github.com/rendiix/termux-apktool
    - install the apktool for your arch then pass it to `apkpatcher` with `--apktool /data/data/com.termux/files/usr/bin/apktool.jar`
 
 - custom zipalign version - https://github.com/rendiix/termux-zipalign
    - it should be automatically detected and used by `apkpatcher`
  

##### APK Patcher Installation
`pip install apkpatcher-cli`

#### How To Use It
For all usages, the output file will be something like <apkname>_patched.apk.

- ##### Bundles
  apkpatcher supports bundles out of the box by just passing the bundle path.

- ##### Inserting Frida Gadget
  ```
  apkpatcher -a base.apk --arch device_architecture
  ```

  If you have adb installed and connected to your device you can ommit the `--arch` argument.

  You can also install a custom gadget by specifying the path to it as:
  ```
  apkpatcher -a base.apk -g ~/Tools/apkpatcher/gadgets/12.5.9/frida-gadget-12.5.9-android-arm.so
  ```

  When you open the app, the Android screen will stay freezed. The frida gadget has started and is waiting for connection. Connect with the command `frida -U -n Gadget`

- ##### Autoload Script
  You can insert the hook script inside the apk and make it load automatically, without requiring to use frida client.
  
  Create the hook script:
  ```
  Java.perform(function(){
      var Log = Java.use('android.util.Log');
      Log.w("FRIDAGADGET", "Hello World");
  });
  ```

  Then use the following command to embed the script in APK:
  ```
  apkpatcher -a base.apk --autoload-script hook.js
  ```

  When you open the app, it will automatically load the hook script.

- ##### Autoload script from frida codeshare
  Same as the above, but this time automatically download the script from [codeshare.frida.re](https://codeshare.frida.re).

  ```
  apkpatcher -a base.apk --codeshare user/hook
  ```

- ##### Load a shared library instead of the frida gadget
  You may also load a custom shared library (e.g compiled with frida-deepfreeze-rs) instead of a frida gadget
  `apkpatcher -a base.apk --lib my_lib.so`

- ##### Enable User Certificate Authorities
  When analyzing android apps, you may want to intercept it's HTTPS traffic with some proxy like Burp Suite. Since Android 7 - Nougat, apps that the target API Level is 24 and above no longer trust user-added CAs. In order to bypass this restriction, you can patch the APK to insert a network configuration. APK Patcher can do this automatically for you. Use the following command

  ```
  apkpatcher --enable-user-certificates --prevent-frida-gadget -a base.apk
  ```
  ~~

  Note that we used the option `--prevent-frida-gadget`, so the frida gadget library is not inserted in the application

  **Caution:** If the network_security_config.xml file already exists, apkpatcher will delete it, and this may cause some bug. APK Patcher will show you the original file content before deleting it.

- ##### Force Extract Resources
  ~~APK Patcher will try the most it can to avoid extracting resource files, since this task may fail sometimes. So if you just want to insert frida gadget and the app already declares the usage of `android.permission.INTERNET`, apkpatcher will not extract AndroidManifest.xml and resource files. It will modify only some smali code.~~
  
  As of 1.2.0 the tool will extract resources by default so the app can install on the device: https://github.com/iBotPeaches/Apktool/issues/1626

- ##### Help during package modification
  Every time you have to modify an APK, it is a tedious task to decompile, modify, repackage, sign (and generate a key if you don't have one), and zipalign it. APK Patcher will help you during this task. You can use the `--wait-before-repackage`, and APK Patcher will wait for you to make any change you want. Then you just instruct APK Patcher to continue, and it will automatically repack the APK, sign it with a randomly generated key, and zipalign it. You can use this option with a combination of other APK Patcher flags.

  - Just decompile and wait for me:
  ```
  apkpatcher -a base.apk --prevent-frida-gadget -w
  ```
  The output will be something like the following:
  ```
  [*] Extracting base.apk (with resources) to /tmp/apkptmp/base
  [*] Some errors may occur while decoding resources that have framework dependencies
  [*] Apkpatcher is waiting for your OK to repackage the apk...
  [*] Are you ready? (y/N):
  ```
  Now you can keep calm, go to `/tmp/apkptmp/base`, modify everything you want and only when you type `y` the APK Patcher will continue:
  ```
  [*] Are you ready? (y/N): y
  [*] Repackaging apk to /tmp/patcher/base_patched.apk
  [*] This may take some time...
  ```
  
- ##### Run shell command before repackage
  You can automate some tasks before repackaging the APK. You can do this with `-x`.
  ```
  apkpatcher -a base.apk -x 'find TMP_PATH_HERE -name *.so' --pass-temp-path
  ```
  And the result will be something similar to this:
  ```
  apkpatcher -a base.apk -x 'find TMP_PATH_HERE -name *.so' --pass-temp-path
  [*] Extracting base.apk (without resources) to /tmp/apkptmp/base
  [*] Copying gadget to /tmp/apkptmp/base/lib/arm64-v8a/libfrida-gadget.so
  [!] Provided shell command: find /tmp/apkptmp/base -name *.so
  [!] Are you sure you want to execute it? (y/N) y
  [*] Executing -> find /tmp/apkptmp/base -name *.so
  /tmp/apkptmp/base/lib/arm64-v8a/libfrida-gadget.so
  /tmp/apkptmp/base/lib/arm64-v8a/libvlcjni.so
  /tmp/apkptmp/base/lib/arm64-v8a/libvlc.so
  /tmp/apkptmp/base/lib/arm64-v8a/libmla.so
  /tmp/apkptmp/base/lib/arm64-v8a/libc++_shared.so
  [*] Repackaging apk to /tmp/patcher/base_patched_15590132979717808.apk
  ```
  Note that you can optionally use the flag `--pass-temp-path` and APK Patcher will replace every instance of `TMP_PATH_HERE` in your command with the path to the temporary directory where the APK was decompiled
