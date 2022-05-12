#ifndef NODE_HPP
#define NODE_HPP

# include <iostream>
# include <string>


class Node
{
    private:
        int     f;
        int     g;
        int     h;
        int     **map;
        void    calculate_f(int **goal_map);
        void    calculate_g(int **goal_map);
        void    calculate_h(int **goal_map);
    public:
        Node();
        Node(int **puzzle, int **goal_map);
        int     get_f(void) const;
        int     get_g(void) const;
        int     get_h(void) const;
        int     **get_map(void) const;
};

#endif