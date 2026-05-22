#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
#include <queue>
#include <stack>
#include <set>
#include <algorithm>
#include <limits>
#include <memory>
#include "nlohmann/json.hpp"

using namespace std;
using json = nlohmann::json;

class GraphNode {
public:
    string name;

    GraphNode(const string& value = "") {
        name = value;
    }
};

class Graph {
protected:
    unordered_map<string, vector<pair<string, int>>> adjacencyList;

public:
    virtual ~Graph() = default;

    void addNode(const string& name) {
        if (!adjacencyList.count(name)) {
            adjacencyList[name] = {};
        }
    }

    void removeNode(const string& name) {
        if (!adjacencyList.count(name)) {
            cout << "Vertex not found\n";
            return;
        }

        adjacencyList.erase(name);

        for (auto& item : adjacencyList) {
            auto& edges = item.second;

            edges.erase(
                remove_if(
                    edges.begin(),
                    edges.end(),
                    [&](const pair<string, int>& edge) {
                        return edge.first == name;
                    }
                ),
                edges.end()
            );
        }
    }

    virtual void addEdge(
        const string& from,
        const string& to,
        int weight = 1
    ) = 0;

    virtual void removeEdge(
        const string& from,
        const string& to
    ) = 0;

    void bfs(const string& start) {
        if (!adjacencyList.count(start)) {
            cout << "Vertex not found\n";
            return;
        }

        set<string> visited;
        queue<string> q;

        visited.insert(start);
        q.push(start);

        cout << "BFS: ";

        while (!q.empty()) {
            string current = q.front();
            q.pop();

            cout << current << " ";

            for (const auto& neighbor : adjacencyList[current]) {
                if (!visited.count(neighbor.first)) {
                    visited.insert(neighbor.first);
                    q.push(neighbor.first);
                }
            }
        }

        cout << "\n";
    }

    void dfs(const string& start) {
        if (!adjacencyList.count(start)) {
            cout << "Vertex not found\n";
            return;
        }

        set<string> visited;
        stack<string> st;

        st.push(start);

        cout << "DFS: ";

        while (!st.empty()) {
            string current = st.top();
            st.pop();

            if (visited.count(current)) {
                continue;
            }

            visited.insert(current);
            cout << current << " ";

            for (
                auto it = adjacencyList[current].rbegin();
                it != adjacencyList[current].rend();
                ++it
            ) {
                if (!visited.count(it->first)) {
                    st.push(it->first);
                }
            }
        }

        cout << "\n";
    }

    void shortestPathBFS(
        const string& start,
        const string& end
    ) {
        if (
            !adjacencyList.count(start) ||
            !adjacencyList.count(end)
        ) {
            cout << "Vertex not found\n";
            return;
        }

        unordered_map<string, bool> visited;
        unordered_map<string, string> parent;

        queue<string> q;

        visited[start] = true;
        q.push(start);

        while (!q.empty()) {
            string current = q.front();
            q.pop();

            for (const auto& neighbor : adjacencyList[current]) {
                if (!visited[neighbor.first]) {
                    visited[neighbor.first] = true;
                    parent[neighbor.first] = current;
                    q.push(neighbor.first);
                }
            }
        }

        if (!visited[end]) {
            cout << "Path not found\n";
            return;
        }

        vector<string> path;

        string current = end;

        while (current != start) {
            path.push_back(current);
            current = parent[current];
        }

        path.push_back(start);

        reverse(path.begin(), path.end());

        cout << "Shortest BFS path: ";

        for (const auto& node : path) {
            cout << node << " ";
        }

        cout << "\n";
    }

    void dijkstra(
        const string& start,
        const string& end
    ) {
        if (
            !adjacencyList.count(start) ||
            !adjacencyList.count(end)
        ) {
            cout << "Vertex not found\n";
            return;
        }

        unordered_map<string, int> distance;
        unordered_map<string, string> parent;

        for (const auto& item : adjacencyList) {
            distance[item.first] = numeric_limits<int>::max();
        }

        distance[start] = 0;

        priority_queue<
            pair<int, string>,
            vector<pair<int, string>>,
            greater<pair<int, string>>
        > pq;

        pq.push({0, start});

        while (!pq.empty()) {
            auto currentData = pq.top();
            pq.pop();

            int currentDistance = currentData.first;
            string currentNode = currentData.second;

            if (currentDistance > distance[currentNode]) {
                continue;
            }

            for (const auto& neighbor : adjacencyList[currentNode]) {
                int newDistance =
                    currentDistance + neighbor.second;

                if (newDistance < distance[neighbor.first]) {
                    distance[neighbor.first] = newDistance;
                    parent[neighbor.first] = currentNode;

                    pq.push({
                        newDistance,
                        neighbor.first
                    });
                }
            }
        }

        if (
            distance[end] ==
            numeric_limits<int>::max()
        ) {
            cout << "Path not found\n";
            return;
        }

        vector<string> path;

        string current = end;

        while (current != start) {
            path.push_back(current);
            current = parent[current];
        }

        path.push_back(start);

        reverse(path.begin(), path.end());

        cout << "Dijkstra path: ";

        for (const auto& node : path) {
            cout << node << " ";
        }

        cout << "\nDistance: "
             << distance[end]
             << "\n";
    }

    void saveToJson(const string& filename) {
        json j;

        for (const auto& item : adjacencyList) {
            for (const auto& edge : item.second) {
                j[item.first].push_back({
                    {"to", edge.first},
                    {"weight", edge.second}
                });
            }
        }

        ofstream file(filename);

        file << j.dump(4);

        file.close();
    }

    void loadFromJson(const string& filename) {
        ifstream file(filename);

        if (!file.is_open()) {
            cout << "File not found\n";
            return;
        }

        json j;
        file >> j;

        adjacencyList.clear();

        for (auto& element : j.items()) {
            string node = element.key();

            adjacencyList[node] = {};

            for (const auto& edge : element.value()) {
                adjacencyList[node].push_back({
                    edge["to"],
                    edge["weight"]
                });
            }
        }

        file.close();
    }

    void printGraph() {
        cout << "Graph:\n";

        for (const auto& item : adjacencyList) {
            cout << item.first << ": ";

            for (const auto& edge : item.second) {
                cout
                    << "("
                    << edge.first
                    << ", "
                    << edge.second
                    << ") ";
            }

            cout << "\n";
        }
    }
};

class DirectedGraph : public Graph {
public:
    void addEdge(
        const string& from,
        const string& to,
        int weight = 1
    ) override {
        if (weight < 0) {
            cout << "Invalid weight\n";
            return;
        }

        addNode(from);
        addNode(to);

        adjacencyList[from].push_back({
            to,
            weight
        });
    }

    void removeEdge(
        const string& from,
        const string& to
    ) override {
        auto& edges = adjacencyList[from];

        edges.erase(
            remove_if(
                edges.begin(),
                edges.end(),
                [&](const pair<string, int>& edge) {
                    return edge.first == to;
                }
            ),
            edges.end()
        );
    }
};

class UndirectedGraph : public Graph {
public:
    void addEdge(
        const string& from,
        const string& to,
        int weight = 1
    ) override {
        if (weight < 0) {
            cout << "Invalid weight\n";
            return;
        }

        addNode(from);
        addNode(to);

        adjacencyList[from].push_back({
            to,
            weight
        });

        adjacencyList[to].push_back({
            from,
            weight
        });
    }

    void removeEdge(
        const string& from,
        const string& to
    ) override {
        auto& first = adjacencyList[from];
        auto& second = adjacencyList[to];

        first.erase(
            remove_if(
                first.begin(),
                first.end(),
                [&](const pair<string, int>& edge) {
                    return edge.first == to;
                }
            ),
            first.end()
        );

        second.erase(
            remove_if(
                second.begin(),
                second.end(),
                [&](const pair<string, int>& edge) {
                    return edge.first == from;
                }
            ),
            second.end()
        );
    }
};

class WeightedGraph : public UndirectedGraph {
};

class GraphFactory {
public:
    static unique_ptr<Graph> createGraph(
        const string& type
    ) {
        if (type == "directed") {
            return make_unique<DirectedGraph>();
        }

        if (type == "undirected") {
            return make_unique<UndirectedGraph>();
        }

        if (type == "weighted") {
            return make_unique<WeightedGraph>();
        }

        return nullptr;
    }
};

int main() {
    unique_ptr<Graph> graph =
        GraphFactory::createGraph("weighted");

    graph->addEdge("A", "B", 4);
    graph->addEdge("A", "C", 2);
    graph->addEdge("B", "D", 5);
    graph->addEdge("C", "D", 1);
    graph->addEdge("D", "E", 3);

    graph->printGraph();

    graph->bfs("A");

    graph->dfs("A");

    graph->shortestPathBFS("A", "E");

    graph->dijkstra("A", "E");

    graph->saveToJson("graph.json");

    unique_ptr<Graph> loadedGraph =
        GraphFactory::createGraph("weighted");

    loadedGraph->loadFromJson("graph.json");

    loadedGraph->printGraph();

    return 0;
}