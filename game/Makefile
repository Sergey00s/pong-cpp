NAME=a.out
SRC=main.cpp Server.cpp
OBJ=$(SRC:.cpp=.o)

CXX=c++


all: $(NAME)



$(NAME): $(OBJ)
	$(CXX) $(OBJ) -o $(NAME)

%.o: %.cpp
	$(CXX) -c $< -o $@


clean:
	rm -f $(OBJ)


fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re