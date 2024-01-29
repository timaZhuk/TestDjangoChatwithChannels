# craete object for Async operations in sockets
from channels.generic.websocket import AsyncWebsocketConsumer
import json
#
class ChatRoomConsumer(AsyncWebsocketConsumer):
    #Connect
    async def connect (self):
        #get information from url root
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # add path to particular caht group for users
        self.room_group_name='chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name, 
            #point for channel_layer instance and channel_name (to consumer)
            self.channel_name

        ) 
        await self.accept()

        
    
    #disconnect
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    #----------PROCESSING DATA FROM--USER INPUT--------------------------------
    #-------receive function
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message=text_data_json['message']
        username=text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            
            {
                'type':'chatroom_message', 
                'message':message,
                'username':username,
            }
        )
    # the same name as type
    async def chatroom_message(self, event):
        message=event['message']
        username=event['username']
        await self.send(text_data=json.dumps(
                {
                    'message':message,
                    'username':username,
                 }
        ))



'''

await self.channel_layer.group_send(
            self.room_group_name,
            
            {
                'type':'tester_message', 
                'tester':'tester'
            }
        )
    # function collect data from 'tester':'tester'
    #'tester_message' is the same as function name
    async def tester_message(self, event):
        #callect the information rhen send the messege via socket
        tester = event['tester']
        await self.send(text_data = json.dumps(
            {
                'tester':tester,
            }
        ))

'''
    
