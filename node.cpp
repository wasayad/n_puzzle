# include "node.hpp"

Node::Node(int **puzzle, int **goal_map)
{
    // this->f = total_cost;
    // this->g = cost_so_far;
    // this->h = estimated_cost;
    this->map = puzzle;
}

void Node::calculate_h() {

    int heuristic = 0;
    for (int i = 0; i < strlen(get_goal_map()); i++) {
        
    }
}

int Node::get_f(void) const
{
    return (this->f);
}

int Node::get_g(void) const
{
    return (this->g);
}

int Node::get_h(void) const
{
    return (this->h);
}

int **Node::get_map(void) const
{
    return (this->map);
}