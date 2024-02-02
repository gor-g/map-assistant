from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from key import openai_key
import json

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai_key,
)




class Conversation:
    HEAD = "Tu es un guide du campus de Bourget du Lac de l'Université Savoie Mont Blanc. Mais l'utilisateur peut te poser des questions sur des endroits qui ne se trouvent pas forcmément sur le campus. Évite les réponses de plus de 50 mots.\nDes codes de location te seront fournit dans la suite. Il s'agit d'un mot anglais décrivant la fonction de l'endroit. Par exmple si un endroit s'applle Mont Du Chat, mais porte le code de location \"university\" tu dois deviner qu'il s'agit d'un endroit en lien avec l'université, mais pas forcément un université et qu'il s'appelle ainsi et que ce n'est pas un montagne réel. Une eception est le code de location \"establishment\" qui est un code générique et signifie que c'est un endroit nommé et non pas une rue par example.\nL'utilisateur va te posser des questions principalement sur des endroits qui ne sont pas très loins du Bourget du lac. Il est probable qu'on te demande une question sur un endroit s'appelant \"rue/avenue/allée/etc. du lac X\" c'est simplement parce que les habitant du Bourget Du Lac ont habitude de nommer leurs rue de cette manière, le nome de la rue ne veux pas dire que celle ci se trouve à proximité du lac X"

    SAVE_FILE_PATH = 'conversation_history_server_final2.txt'

    def __init__(self, messages = None):
        if messages is None:
            self._messages = []
            self._messages_for_user = []
            self.appends(Conversation.HEAD)
        else:
            assert type(messages) == list and all(type(m)==dict for m in messages)
            self._messages = messages
            self.compute_messages_for_user()

    @property
    def messages(self):
        return self._messages

    @property
    def messages_for_user(self):
        return self._messages_for_user

    def __str__(self):
        return "\n".join(m["role"] + " : " + m["content"] for m in self._messages)

    def __eq__(self, other):
        if isinstance(other, Conversation):
            return self._messages == other.messages
        return False

    def compute_messages_for_user(self):
        self._messages_for_user = []
        i=0
        exchange = dict()
        while i < len(self._messages):
            m = self._messages[i]
            if m["role"] == "user":
                exchange = {"user": m["content"]}
            elif m["role"] == "assistant":
                assert list(exchange.keys()) == ["user"]
                exchange["assistant"] = m["content"]
                self._messages_for_user.append(exchange)
            i+=1
        if list(exchange.keys()) == ["user"]:
            self._messages_for_user.append(exchange)
        else:
            print(list(exchange.keys()))

    def update_messages_for_user(self, role, content):
        if role == "user":
            if len(self._messages_for_user):
                #BEGIN TEST
                temp = list(self._messages_for_user[-1].keys())
                assert temp == ["user", "assistant"] or temp == ["assistant", "user"]
                #END TEEST
            self._messages_for_user.append({"user":content})
        else:
            assert role == "assistant"
            # BEGIN TEST
            assert list(self._messages_for_user[-1].keys()) == ["user"]
            # END TEEST

            self._messages_for_user[-1]["assistant"] = content

    def append(self, role: str, message: str):
        assert role in ["assistant", "user", "system"], "Unknown role %s" % role
        self._messages.append({"role": role, "content": message})

        if role != "system":
            self.update_messages_for_user(role, message)

        # BEGIN TEST
        mfu = self._messages_for_user
        self.compute_messages_for_user()
        assert mfu == self._messages_for_user, str(mfu) + ":" + str(self._messages_for_user)
        # END TEST

        print("new message : ", self._messages[-1])

    def appenda(self, message: str):
        """append assistant message"""
        self.append("assistant", message)

    def appendu(self, message: str):
        """append user message"""
        self.append("user", message)

    def appends(self, message: str):
        """append system message"""
        self.append("system", message)

    def appendc(self, message: ChatCompletion):
        """append message from a ChatCompletion object"""

        m = message.choices[0].message
        assert m.role == "assistant", "received answer has an unexpected role '%s'" % m.role

        self.appenda(m.content)



    def append_location_description_request(self, system_message: str, user_message: str):
        self.appends(system_message)
        self.appendu(user_message)

    def complete(self):
        assert self._messages[-1]["role"] != "assistant", ("Tried to send a message list where the last message came "
                                                           "from the assistant")

        chat_completion = client.chat.completions.create(
                                                            messages=self._messages,
                                                            model="gpt-3.5-turbo",
                                                        )

        self.appendc(chat_completion)
        return self._messages[-1]["content"]


    def load(self):
        try:
            with open(self.SAVE_FILE_PATH, 'r') as file:
                self._messages = json.load(file)
                self.compute_messages_for_user()
        except (json.JSONDecodeError, FileNotFoundError):
            self.dump()

    def dump(self):
        with open(self.SAVE_FILE_PATH, 'w') as file:
            json.dump(self._messages, file)
        

if __name__ == "__main__":
    # c1 = Conversation()
    ms = "L'utilisateur est interessé par l'endroit qui s'appelle \"Polytech Annecy-Chambéry\". L'endroit porte les codes de location \"university\", \"point_of_interest\", \"establishment\". L'endroit est actuellement fermé. L'endroit est noté 3.9 sur 5 sur google. L'endroit se trouve à proximité de 2 Avenue du Lac d'Annecy, Le Bourget-du-Lac."
    mu = "Décrit l'endroit \"Polytech Annecy-Chambéry\"."
    # c1.appends(ms)
    # c1.appendu(mu)
    # c2 = Conversation()
    # c2.addDescriptionRequest(ms, mm)
    # assert c1 == c2
    #
    # print(c1)

    c = Conversation()
    c.append_location_description_request(ms, mu)
    c.complete()
    user_input = mu
    while True:
        user_input = input()
        if user_input == "q":
            break
        c.appendu(user_input)
        c.complete()

    print(c)
