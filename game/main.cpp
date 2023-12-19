
#include "Server.h"



int main(int argc, char const *argv[])
{
	Server server(2700);

	while (true)
	{

		if (server.update())
		{
			if (FD_ISSET(server.getServerFd(), &server.getReadfds()))
			{
				int new_socket = server.acceptConnection();
				server.getClients().push_back(new_socket);
				std::cout << "New connection" << std::endl;
			}
			server.recive_messages(server.messages);
		}
	}
	return 0;
}


