import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MyRoot(BoxLayout):
    def __init_(self):
        super(MyRoot, self).__init_()

    def show_card(self):
        self.card_label.text = str('XAXA')


class FlashCard(App):

    def build(self):
        return MyRoot()


FlashCard = FlashCard()
FlashCard.run()
