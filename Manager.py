import ast

class DownloadManager():
    def __init__(self,prop):
        self.prop = prop
        pass
    def get_provide(self,link):
        if "youtube" in link.split(".") or "youtu.be" in link.split("."):
            return YouTubeProvide(self.prop)

if __name__ == "__main__":
    with open('propeties.cfg', 'r', encoding='utf-8') as f:
        file = f.read()
        prop = ast.literal_eval(file)
        