import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    comp_list = []
    def connect(self):
        self.room_group_name = 'room'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print(self.comp_list)
        print("User connected")
 

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.comp_list = []
        print("User disconnected")
 
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            fields_data = text_data_json['fields_data']
            print(fields_data)
            #if '' not in fields_data: fields_data = "Игра закончена"
        
            #По квадрату

            winn_combo_1 = [fields_data[0], fields_data[1], fields_data[2]]
            winn_combo_result_1 = [0,1,2]
            winn_combo_2 = [fields_data[0], fields_data[3], fields_data[6]]
            winn_combo_result_2 = [0,3,6]
            winn_combo_3 = [fields_data[6], fields_data[7], fields_data[8]]
            winn_combo_result_3 = [6,7,8]
            winn_combo_4 = [fields_data[2], fields_data[5], fields_data[8]]
            winn_combo_result_4 = [2,5,8]

            #По кресту угловому
            winn_combo_5 = [fields_data[0], fields_data[4], fields_data[8]]
            winn_combo_result_5 = [0,4,8]
            winn_combo_6 = [fields_data[2], fields_data[4], fields_data[6]]
            winn_combo_result_6 = [2,4,6]

            #По кресту прямому
            winn_combo_7 = [fields_data[1], fields_data[4], fields_data[7]]
            winn_combo_result_7 = [1,4,7]
            winn_combo_8 = [fields_data[3], fields_data[4], fields_data[5]]
            winn_combo_result_8 = [3,4,5]

            cheat_array = [winn_combo_1,winn_combo_2,winn_combo_3,winn_combo_4,winn_combo_5,winn_combo_6,winn_combo_7,winn_combo_8]

            end_game = None
            #По квадрату
            if all(v =="X"  for v in  winn_combo_1 ):
                end_game = "Конец"
                result_game = winn_combo_result_1 
                print("1")
                print(winn_combo_1)
            elif all(v =="X" for v in winn_combo_2):
                end_game = "Конец"
                result_game = winn_combo_result_2 
                print("2")
            elif all(v =="X" for v in winn_combo_3):
                end_game = "Конец"
                result_game = winn_combo_result_3 
                print("3")
            elif all(v =="X" for v in winn_combo_4):
                end_game = "Конец"
                result_game = winn_combo_result_4 
                print("4")
            #По кресту угловому
            elif all(v =="X" for v in winn_combo_5):
                end_game = "Конец"
                result_game = winn_combo_result_5 
                print("5")
            elif all(v =="X" for v in winn_combo_6):
                end_game = "Конец"
                result_game = winn_combo_result_6 
                print("6")
            #По кресту прямому
            elif all(v =="X" for v in winn_combo_7):
                end_game = "Конец"
                result_game = winn_combo_result_7 
                print("7")
            elif all(v =="X" for v in winn_combo_8):
                end_game = "Конец"
                result_game = winn_combo_result_8 
                print("8")


            #По квадрату
            if all(v =="O"  for v in winn_combo_1):
                end_game = "Конец"
                result_game = winn_combo_result_1
                print("1")
            elif all(v =="O" for v in winn_combo_2):
                end_game = "Конец"
                result_game = winn_combo_result_2
                print("2")
            elif all(v =="O" for v in winn_combo_3):
                end_game = "Конец"
                result_game = winn_combo_result_3
                print("3")
            elif all(v =="O" for v in winn_combo_4):
                end_game = "Конец"
                result_game = winn_combo_result_4
                print("4")
            #По кресту угловому
            elif all(v =="O" for v in winn_combo_5):
                end_game = "Конец"
                result_game = winn_combo_result_5
                print("5")
            elif all(v =="O" for v in winn_combo_6):
                end_game = "Конец"
                result_game = winn_combo_result_6
                print("6")
            #По кресту прямому
            elif all(v =="O" for v in winn_combo_7):
                end_game = "Конец"
                result_game = winn_combo_result_7
                print("7")
            elif all(v =="O" for v in winn_combo_8):
                end_game = "Конец"
                result_game = winn_combo_result_8
                print("8")


            if end_game != "Конец":
                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'enter_signal',
                        'data_fields': fields_data,
                    }
                )
            elif end_game == "Конец":
                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'enter_end_signal',
                        'end_game_result': result_game,
                        'end_game_signal' : end_game,
                        'data_fields': fields_data,
                    }
                )

        except :
            nickname = text_data_json['nickname']
            user_wep = text_data_json['user_wep']

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'pre_game_signal',
                    'nickname': nickname,
                    'user_wep': user_wep,
                }
            )

    def pre_game_signal(self, event):
        nickname = event['nickname']
        user_wep = event['user_wep']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'nickname': nickname,
            'user_wep': user_wep,
        }))

    def enter_end_signal(self, event):
        data_fields = event['data_fields']
        end_game = event['end_game_signal']
        end_game_result = event['end_game_result']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'end_game_signal' : end_game,
            'end_game_result' : end_game_result,
            'data_fields': data_fields,
        }))

    def enter_signal(self, event):
        data_fields = event['data_fields']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'data_fields': data_fields,
        }))