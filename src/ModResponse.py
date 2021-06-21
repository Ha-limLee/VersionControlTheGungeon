class ModResponse:
    def __init__(self, id: str, response):
        self.id = id
        self.response = response
        pass

    def getContent(self):
        return self.response.content

    def getId(self):
        return self.id

    def getName(self):
        '''
        returns file name
        e.g. 111111_mod_0.1.zip
        '''
        header = self.response.headers
        # 'Content-disposition': 'attachment; filename=[filename]'
        # filename braced with ""
        return header['content-disposition'].split('filename=')[1].strip('\"')

    def getDate(self):
        header = self.response.headers
        
        last_modified = header['Last-Modified']
        # it will be used to check version

        print(last_modified)
        return last_modified