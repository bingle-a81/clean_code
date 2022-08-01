
class Server:
    """для описания работы серверов в сети
    Соответственно в объектах класса Server должны быть локальные свойства:
    buffer - список принятых пакетов (изначально пустой);
    ip - IP-адрес текущего сервера.
    """
    server_ip=1
    def __init__(self) -> None:
        self.buffer=[]
        self.ip=Server.server_ip
        Server.server_ip+=1
        self.router=None


    def send_data(self,data):
        """для отправки информационного пакета data (объекта класса Data) 
        с указанным IP-адресом получателя (пакет отправляется роутеру и 
        сохраняется в его буфере - локальном свойстве buffer);
        """
        if self.router:
            self.router.buffer.append(data)

    def get_data(self):
        """возвращает список принятых пакетов (если ничего принято не было, 
        то возвращается пустой список) и очищает входной буфер;
        """
        d=self.buffer[:]
        self.buffer.clear()
        return d

    def get_ip(self):
        """возвращает свой IP-адрес.
        """
        return self.ip


class Router:
    """для описания работы роутеров в сети (в данной задаче полагается один роутер).
    И одно обязательное локальное свойство (могут быть и другие свойства):
    buffer - список для хранения принятых от серверов пакетов (объектов класса Data).
    """
    def __init__(self) -> None:
        self.buffer=[]
        self.servers={}
    
    def link(self,server):
        """для присоединения сервера server (объекта класса Server) к роутеру
        """
        self.servers[server.ip]=server
        server.router=self
    
    def unlink(self,server):
        """для отсоединения сервера server (объекта класса Server) от роутера
        """
        s=self.servers.pop(server.ip,False)
        if s:
            s.router=None
    
    def send_data(self):
        """для отправки всех пакетов (объектов класса Data) из буфера роутера 
        соответствующим серверам (после отправки буфер должен очищаться)
        """
        for d in self.buffer:
            if d.ip in self.servers:
                self.servers[d.ip].buffer.append(d)
        self.buffer.clear()
    

class Data:
    """для описания пакета информации
    Наконец, объекты класса Data должны содержать, два следующих локальных свойства:
    data - передаваемые данные (строка);
    ip - IP-адрес назначения.
    """
    def __init__(self,msg,ip) -> None:
        
        self.data=msg
        self.ip=ip

def main():
    assert hasattr(Router, 'link') and hasattr(Router, 'unlink') and hasattr(Router, 'send_data'),"в \
    классе Router присутсвутю не все методы, указанные в задании"
    assert hasattr(Server, 'send_data') and hasattr(Server, 'get_data') and hasattr(Server, 'get_ip'), "в \
    классе Server присутсвутю не все методы, указанные в задании"
    router = Router()
    sv_from = Server()
    sv_from2 = Server()
    router.link(sv_from)
    router.link(sv_from2)
    router.link(Server())
    router.link(Server())
    sv_to = Server()
    router.link(sv_to)
    sv_from.send_data(Data("Hello", sv_to.get_ip()))
    sv_from2.send_data(Data("Hello", sv_to.get_ip()))
    sv_to.send_data(Data("Hi", sv_from.get_ip()))
    router.send_data()
    msg_lst_from = sv_from.get_data()
    msg_lst_to = sv_to.get_data()

    assert len(router.buffer) == 0, "после отправки сообщений буфер в роутере должен очищаться"
    assert len(sv_from.buffer) == 0, "после получения сообщений буфер сервера должен очищаться"

    assert len(msg_lst_to) == 2, "метод get_data вернул неверное число пакетов"

    assert msg_lst_from[0].data == "Hi" and msg_lst_to[0].data == "Hello", "данные не прошли по сети, классы не функционируют должным образом"

    assert hasattr(router, 'buffer') and hasattr(sv_to, 'buffer'), "в объектах классов Router и/или Server отсутствует локальный атрибут buffer"

if __name__ == "__main__":
    main()
