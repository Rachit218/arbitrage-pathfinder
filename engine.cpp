#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <cmath>
#include <map>
#include <algorithm>
#include <limits>
using namespace std;

struct Edge{
    int source;
    int target;
    double original_rate;
    double weight;
};

vector<string> parse_csv_line(const string& line){
    vector<string> result;
    stringstream ss(line);
    string cell;
    while (getline(ss,cell,',')){
        result.push_back(cell);
    }
    return result;
}

int main(){
    ifstream file("market_edges.csv");
    if (!file.is_open()){
        cout << "Could not open file" << endl;
        return 1;
    }
    map<string,int> currency_to_id;
    map<int,string> id_to_currency;
    vector<Edge> edges;
    int current_id = 0;
    string line;
    getline(file,line);
    
    // Parsing through the csv and building the required graph
    while(getline(file,line)){
        if (line.empty()) continue;
        auto tokens = parse_csv_line(line);
        if (tokens.size()<3) continue;
        string source_string = tokens[0];
        string dest_string = tokens[1];
        double rate = stod(tokens[2]);
        if (currency_to_id.find(source_string) == currency_to_id.end()){
            currency_to_id[source_string] = current_id;
            id_to_currency[current_id] = source_string;
            current_id++;
        }
        if (currency_to_id.find(dest_string) == currency_to_id.end()){
            currency_to_id[dest_string] = current_id;
            id_to_currency[current_id] = dest_string;
            current_id++;
        }
        int u = currency_to_id[source_string];
        int v = currency_to_id[dest_string];
        double log_rate = -log(rate);
        edges.push_back({u,v,rate,log_rate});
    }
    file.close();
    int V = current_id;
    if (V == 0) return 0;

    vector<double> dist(V,numeric_limits<double>::infinity());
    vector<int> parent(V,-1);
    dist[0] = 0;

    for(int i =0 ; i<V-1;i++){
        for(const auto& edge:edges){
            if(dist[edge.source] != numeric_limits<double>::infinity()){
                if (dist[edge.source] + edge.weight < dist[edge.target]) {
                    dist[edge.target] = dist[edge.source] + edge.weight;
                    parent[edge.target] = edge.source;
            }
            }
        }
    }

    int cycle_node = -1;
    for (const auto& edge : edges) {
        if (dist[edge.source] != std::numeric_limits<double>::infinity()) {
            if (dist[edge.source] + edge.weight < dist[edge.target]) {
                cycle_node = edge.target;
                parent[edge.target] = edge.source; 
                break;
            }
        }
    }
    if (cycle_node == -1) {
        std::cout << "STATUS: Stable Market. No cycles detected across " << V << " currencies.\n";
        return 0;
    }
    
    int curr = cycle_node;
    for (int i = 0; i < V; ++i) {
        curr = parent[curr];
    }
    int start_node = curr;
    vector<int> cycle_path;
    cycle_path.push_back(curr);
    curr = parent[start_node];
    while (curr != start_node){
        cycle_path.push_back(curr);
        curr = parent[curr];
    }
    cycle_path.push_back(start_node);
    reverse(cycle_path.begin(),cycle_path.end());
    cout << "ARBITRAGE DETECTED\n";
    cout << "Sequence: ";
    double net_multiplier = 1.0;
    
    for (int i = 0; i < cycle_path.size() - 1; ++i) {
        int u = cycle_path[i];
        int v = cycle_path[i+1];
        std::cout << id_to_currency[u] << " -> ";
        
        for (const auto& edge : edges) {
            if (edge.source == u && edge.target == v) {
                net_multiplier *= edge.original_rate;
                break;
            }
        }
    }
    cout << id_to_currency[cycle_path.back()] << "\n";
    cout << "Compounded Return Rate: " << net_multiplier << "x\n";
    cout << "Net Profit: " << (net_multiplier - 1.0) * 100.0 << "%\n";

    return 0;
}