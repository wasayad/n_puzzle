#ifndef SOLVER_HPP
#define SOLVER_HPP

# include <iostream>
# include <string>
# include "node.hpp"
# include "vector"

class Solver 
{
    private:
        Solver();
        Node                start;
        std::vector<Node>   open_list;
        std::vector<Node>   closed_list;
        std::vector<Node>   generate_child(Node parent);
        bool                check_in_list(Node to_add, std::vector<Node> list);
        int                 get_best_path(void);
    public:
        Solver(Node start_node);

};

#endif