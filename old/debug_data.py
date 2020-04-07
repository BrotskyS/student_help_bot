class Message:
    chat = type('obj', (object,), {'id' : '123'})
    
    def __init__(self, m_id, g_id=None, photo=None, caption=None, text=None):
        self.media_group_id = g_id
        self.message_id = m_id
        self.caption = caption
        self.text = text
        self.photo = [type('obj', (object,), {'file_id' : photo})] if photo else []

ml = [
    Message(m_id=55, g_id=334456, photo='FirstPhotoIDqy0wt7eteq26@#$b43f87g', caption='05/12'),
    Message(m_id=555, g_id=334456, photo='SecondPhotoIDqywteteq26@$~35x3b45feg'),
    Message(m_id=17, text='some homework for 12/08'),
    Message(m_id=13, text='дз 05/12'),
    Message(m_id=536, g_id=4534456, photo='thirdPhotoIDqywteteq26@#$', caption='07/12'),
    Message(m_id=456, g_id=4534456, photo='FourthPhotoIDqywteteq26@#$'),
    Message(m_id=12, text='дз 12/08'),
]