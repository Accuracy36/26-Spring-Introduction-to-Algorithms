#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
const ll INF = 1e18;

struct Edge {
    int to;
    ll cap;
    ll flow;
    int rev;
};

struct Dinic {
    int n;
    vector<vector<Edge>> adj;
    vector<int> level;
    vector<int> ptr;

    Dinic(int n) : n(n), adj(n), level(n), ptr(n) {}

    void addEdge(int u, int v, ll w) {
        adj[u].push_back({v, w, 0, (int)adj[v].size()});
        adj[v].push_back({u, w, 0, (int)adj[u].size() - 1});
    }

    void resetFlow() {
        for (int i = 0; i < n; i++) {
            for (auto& edge : adj[i]) {
                edge.flow = 0;
            }
        }
    }

    bool bfs(int s, int t) {
        fill(level.begin(), level.end(), -1);
        level[s] = 0;
        queue<int> q;
        q.push(s);
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (auto& edge : adj[v]) {
                if (edge.cap - edge.flow > 0 && level[edge.to] == -1) {
                    level[edge.to] = level[v] + 1;
                    q.push(edge.to);
                }
            }
        }
        return level[t] != -1;
    }

    ll dfs(int v, int t, ll pushed) {
        if (pushed == 0) return 0;
        if (v == t) return pushed;
        for (int& cid = ptr[v]; cid < adj[v].size(); ++cid) {
            auto& edge = adj[v][cid];
            int tr = edge.to;
            if (level[v] + 1 != level[tr] || edge.cap - edge.flow == 0) continue;
            ll push = dfs(tr, t, min(pushed, edge.cap - edge.flow));
            if (push == 0) continue;
            edge.flow += push;
            adj[tr][edge.rev].flow -= push;
            return push;
        }
        return 0;
    }

    ll maxFlow(int s, int t) {
        ll flow = 0;
        while (bfs(s, t)) {
            fill(ptr.begin(), ptr.end(), 0);
            while (ll pushed = dfs(s, t, INF)) {
                flow += pushed;
            }
        }
        return flow;
    }

    vector<int> getCut(int s) {
        vector<int> visited(n, 0);
        queue<int> q;
        q.push(s);
        visited[s] = 1;
        vector<int> cut_set;
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            cut_set.push_back(u);
            for (auto& edge : adj[u]) {
                if (edge.cap - edge.flow > 0 && !visited[edge.to]) {
                    visited[edge.to] = 1;
                    q.push(edge.to);
                }
            }
        }
        return cut_set;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;
    
    Dinic dinic(n + 1);
    
    for (int i = 0; i < m; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        dinic.addEdge(u, v, w);
    }

    ll min_cut = INF;
    vector<int> best_cut_set;

    for (int t = 2; t <= n; t++) {
        dinic.resetFlow();
        ll current_flow = dinic.maxFlow(1, t);
        if (current_flow < min_cut) {
            min_cut = current_flow;
            best_cut_set = dinic.getCut(1);
        }
    }

    cout << min_cut << "\n";
    cout << best_cut_set.size();
    for (int i = 0; i < best_cut_set.size(); i++) {
        cout << " " << best_cut_set[i];
    }
    cout << "\n";
    
    return 0;
}