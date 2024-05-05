from flask import Flask, render_template, request

print('Welcome to the goofy encoder!')

# unicode zero width space character are: \u200b and \u200c
# \u200b is a zero width space
# \u200c is a zero width non-joiner

def encode(message):
    secret = "$"
    for char in message:
        # get binary representation of the character
        binary = str(bin(ord(char))[2:])
        # if it's a 0, convert it to a zero width space
        for i in binary:
            if i == '0':
                secret += '\u200b'
            else:
                secret += '\u200c'
        secret += '$'
    return secret + '$'


def decode(message):
    clear = ''
    # remove the first and last character, which are dollar signs
    message = message[1:-1]
    # split the message into the individual characters
    characters = message.split('$')
    # remove the last character, which is an empty string
    characters.pop()
    while '' in characters:
        characters.remove('')
    # for each character, convert it to a binary representation
    for char in characters:
        binary = ''
        for i in char:
            if i == '\u200b':
                binary += '0'
            else:
                binary += '1'
        # convert the binary representation to a character
        clear += chr(int(binary, 2))
    return clear


def wrapEncode(message, wrapper):
    # wrap the encoded message in another message
    encoded = encode(message)
    #wrapper = input('Enter the message you want to wrap the encoded message in: ')
    if len(wrapper) != encoded.count('$')-2:
        # pad the wrapper with dots
        while len(wrapper) <= encoded.count('$')-2:
            wrapper += '.'
    wrapped = ''
    bits = encoded.split('$')
    # remove first element, which is an empty string
    bits.pop(0)
    # remove last 2 elements, which are an empty string
    bits.pop()
    bits.pop()
    for i in range(len(bits)):
        wrapped += wrapper[i] + bits[i]
    return wrapped + wrapper[len(wrapped.replace('\u200b', '').replace('\u200c', '')):]


def wrapDecode(message):
    pog = ''
    temp = []
    # group the zero width characters each group being the one separated by a non zero width character
    for i in range(len(message)):
        if message[i] == '\u200b' or message[i] == '\u200c':
            pog += message[i]
        else:
            temp.append(pog)
            pog = ''
    # remove empty elements
    while '' in temp:
        temp.remove('')
    dec = ''
    for char in temp:
        binary = ''
        for i in char:
            if i == '\u200b':
                binary += '0'
            else:
                binary += '1'
        # convert the binary representation to a character
        dec += chr(int(binary, 2))
    return dec


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encode', methods=['POST'])
def encodeWeb():
    message = request.form['message']
    wrapper = request.form['wrapper']
    #print(type(message))
    message = wrapEncode(message, wrapper)
    return render_template('encode.html', message=message)


@app.route('/decode', methods=['POST'])
def decode():
    message = request.form['message']
    message = wrapDecode(message)
    return render_template('decode.html', message=message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6969)

# run the website with: python main.py (unless you're cringe and still use python2, then use python3 main.py)
