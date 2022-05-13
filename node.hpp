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
        int     **goal_map;

        Node();
        void    calculate_f(void);
        void    calculate_g(void); // blc normalement de ça
        void    calculate_h(void);
    public:
        Node(int **puzzle, int **goal_map);
        int     get_f(void) const;
        int     get_g(void) const;
        int     get_h(void) const;
        int     **get_map(void) const;
        int     **get_goal_map(void) const;
};

#endif