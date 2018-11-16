import frida
import sys
import time


def on_message(message, data):
    try:
        if message:
            print("[*] Received data: {0}".format(message["payload"]))
    except Exception as e:
        print(message)
        print(e)


def run_frida_script():
    frida_script_code = """

        console.log("Script loaded successfully ");

        Java.perform(function x()
        { 
        console.log("Inside java perform function");

        var my_class = Java.use("hsbc.rick.frida_practice.FirstActivity");

        my_class.fun.implementation = function(x,y){
        console.log( "original call: fun("+ x + ", " + y + ")");
        var ret_value = this.fun(2,5);

        return ret_value;}
        
        });


        """
    print('[*] Executing frida code:\n')
    return frida_script_code


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print("Usage:" + sys.argv[0] + "<process_name> <local|usb>")
        sys.exit(1)
    try:
        session = None
        if (sys.argv[2] == "local"):
            # For local connection
            session = frida.attach(sys.argv[1])
        elif (sys.argv[2] == "usb"):
            # For USB connection
            device = frida.get_usb_device()
            pid = device.spawn(sys.argv[1])
            time.sleep(1) #Without it Java.perform silently fails
            session = device.attach(pid)
            device.resume(pid)
        else:
            # Invalid connection choice
            print("Usage:" + sys.argv[0] + "<process_name> <local|usb>")
            sys.exit(1)

        script = session.create_script(run_frida_script())
        script.on('message', on_message)
        script.load()
        sys.stdin.read()
    except KeyboardInterrupt:
        sys.exit(0)