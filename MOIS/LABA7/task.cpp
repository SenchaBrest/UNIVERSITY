#include "../graph_LIB.hh"

void test(std::string file_path1, std::string file_path2)
{
	convert c;
    
    std::vector<std::string> nodes1, nodes2;
    nodes1 = c.reading_file_symb(file_path1);
    nodes2 = c.reading_file_symb(file_path2);
    tree_symb tree1, tree2;
    for(int i = 0; i < nodes1.size(); i += 2)
    {
        tree1.add_node(nodes1[i], nodes1[i + 1]);
    }
    for(int i = 0; i < nodes2.size(); i += 2)
    {
        tree2.add_node(nodes2[i], nodes2[i + 1]);
    }
    tree1.print_tree();
    std::cout << std::endl << std::endl;
    tree2.print_tree();
    std::cout << std::endl << std::endl;
    
    std::cout << "T1 height : " << tree1.height(tree1.get_root()) << std::endl;
    std::cout << "T2 height : " << tree2.height(tree2.get_root()) << std::endl;
    std::cout << std::endl << std::endl;

    std::cout << "T1 is balanced? : " << tree1.isBalanced(tree1.get_root()) << std::endl;
    std::cout << "T2 is balanced? : " << tree2.isBalanced(tree2.get_root()) << std::endl;

    alg a;
    bool check = a.is_isomorphic(tree1.get_root(), tree2.get_root());
    std::cout << "Isomorphic? : " << check;
    std::cout << std::endl << std::endl;

    a.try2make_isomorphic(tree1, tree2);
    
    tree1.print_tree();
    std::cout << std::endl << std::endl;
    tree2.print_tree();
    std::cout << std::endl << std::endl;

    check = a.is_isomorphic(tree1.get_root(), tree2.get_root());
    std::cout << "Isomorphic? : " << check;
    std::cout << std::endl << std::endl;

}

int main()
{
    int v = 5;
    test("T1/T1v" + std::to_string(v) + ".txt", "T2/T2v" + std::to_string(v) + ".txt");
}