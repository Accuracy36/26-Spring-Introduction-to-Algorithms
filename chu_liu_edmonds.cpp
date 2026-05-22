#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
const ll INF = 1e18;

// 定义有向边结构体
struct Edge {
    int u, v, id;
    ll w;
};

class ChuLiuEdmonds {
private:
    int n, root;
    vector<Edge> edges;
    
public:
    // 构造函数初始化节点数和根节点
    ChuLiuEdmonds(int n, int root) : n(n), root(root) {}
    
    // 添加有向边
    void addEdge(int u, int v, ll w, int id) {
        edges.push_back({u, v, id, w});
    }
    
    // 对外接口
    pair<ll, vector<int>> solve() {
        return solveRec(n, root, edges);
    }
    
private:
    // 核心递归函数：返回值为 {最小总边权, 选中的边编号列表}
    pair<ll, vector<int>> solveRec(int cur_n, int cur_root, const vector<Edge>& cur_edges) {
        // minOut[i] 记录节点 i 选中的最小出边在 cur_edges 中的索引
        vector<int> minOut(cur_n, -1);
        // minCost[i] 记录节点 i 选中的最小出边的权值
        vector<ll> minCost(cur_n, INF);
        
        // 1. 为每个非根节点寻找最小权值的出边（严格对应题目要求）
        for (int i = 0; i < cur_edges.size(); i++) {
            int u = cur_edges[i].u;
            // 忽略自环，并且根节点不需要出边
            if (u != cur_edges[i].v && u != cur_root && cur_edges[i].w < minCost[u]) {
                minCost[u] = cur_edges[i].w;
                minOut[u] = i;
            }
        }
        
        // 检查连通性：如果某个非根节点没有出边，说明无法到达根节点，无解
        for (int i = 0; i < cur_n; i++) {
            if (i != cur_root && minOut[i] == -1) {
                return {-1, {}};
            }
        }
        
        // 2. 寻找有向环（使用访问标记而非并查集，精确找环）
        vector<int> vis(cur_n, -1);
        int cycle_start = -1; // 记录环的起点
        
        for (int i = 0; i < cur_n; i++) {
            if (i == cur_root) continue;
            int curr = i;
            // 顺着最小出边不断前进，直到走到根节点或遇到已访问过的节点
            while (curr != cur_root && vis[curr] == -1) {
                vis[curr] = i; // 标记为在第 i 次搜索中被访问
                curr = cur_edges[minOut[curr]].v;
            }
            // 如果遇到的是本次搜索刚刚标记的节点，说明找到了一个环！
            if (curr != cur_root && vis[curr] == i) {
                cycle_start = curr;
                break; // 每次递归只处理一个环即可，剩下的交给后续递归
            }
        }
        
        // 如果图中没有环，说明当前选出的边已经构成了最小树形图！直接返回。
        if (cycle_start == -1) {
            ll total = 0;
            vector<int> res;
            for (int i = 0; i < cur_n; i++) {
                if (i != cur_root) {
                    res.push_back(cur_edges[minOut[i]].id);
                    total += minCost[i];
                }
            }
            return {total, res};
        }
        
        // 3. 将环上的节点提取出来并标记
        vector<bool> inCycle(cur_n, false);
        int temp = cycle_start;
        do {
            inCycle[temp] = true;
            temp = cur_edges[minOut[temp]].v;
        } while (temp != cycle_start);
        
        // 4. 将环缩成一个新点，重新分配节点 ID
        vector<int> oldToNew(cur_n, -1);
        int new_n = 0;
        int new_cycle_id = -1; // 缩点后的新环 ID
        
        for (int i = 0; i < cur_n; i++) {
            if (inCycle[i]) {
                // 环上的所有节点都映射到同一个新 ID
                if (new_cycle_id == -1) new_cycle_id = new_n++;
                oldToNew[i] = new_cycle_id;
            } else {
                // 不在环上的节点分配独立的新 ID
                oldToNew[i] = new_n++;
            }
        }
        
        int new_root = oldToNew[cur_root]; // 映射新的根节点
        vector<Edge> newEdges; // 存储缩点后的新边
        
        for (int i = 0; i < cur_edges.size(); i++) {
            int u = cur_edges[i].u;
            int v = cur_edges[i].v;
            int nu = oldToNew[u];
            int nv = oldToNew[v];
            
            // 忽略缩点后形成的新自环（即原先环内部的边）
            if (nu == nv) continue;
            
            ll new_w = cur_edges[i].w;
            // 核心逻辑：如果边是从环内某个点 u 离开环的，新边的权值需要减去 out[u] 的权值
            if (inCycle[u] && !inCycle[v]) {
                new_w -= minCost[u];
            }
            // 边的 ID 保持不变，用于最终还原
            newEdges.push_back({nu, nv, cur_edges[i].id, new_w});
        }
        
        // 5. 在缩点后的新图上递归执行上述过程
        auto [subCost, subRes] = solveRec(new_n, new_root, newEdges);
        
        // 如果缩点图无解，原图也无解
        if (subCost == -1) return {-1, {}};
        
        // 6. 展开环：还原当前层的边
        int orig_u_leaving = -1; // 记录是从环上哪个原始点离开的
        vector<int> res;
        
        // 将递归返回的边原封不动地加入答案
        for (int eid : subRes) {
            res.push_back(eid);
            // 通过边 ID 找到这条边在当前层的具体起点
            for (const auto& e : cur_edges) {
                if (e.id == eid) {
                    if (inCycle[e.u]) {
                        orig_u_leaving = e.u; // 找到了替代环上 out 边的那条外部边
                    }
                    break;
                }
            }
        }
        
        // 计算真实代价并补全环内的边
        // 因为前面离开环的边扣除了 minCost[orig_u_leaving]，为了凑齐原边权，我们需要加回所有环节点的 minCost
        for (int i = 0; i < cur_n; i++) {
            if (inCycle[i]) {
                subCost += minCost[i]; // 无脑加上环上所有的出边权值，从数学上正好抵消之前的减法
                // 除了被外部边替代的那个点，其他环上的点依然使用它们原来的最小出边
                if (i != orig_u_leaving) {
                    res.push_back(cur_edges[minOut[i]].id);
                }
            }
        }
        
        return {subCost, res};
    }
};

int main() {
    // 优化输入输出速度
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, m, r;
    if (!(cin >> n >> m >> r)) return 0;
    r--; // 转换为 0-indexed，方便数组操作
    
    ChuLiuEdmonds solver(n, r);
    
    for (int i = 0; i < m; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        u--; v--; // 转换为 0-indexed
        solver.addEdge(u, v, w, i + 1); // 传入 1-indexed 的边编号 i+1
    }
    
    auto result = solver.solve();
    ll cost = result.first;
    vector<int> edges = result.second;
    
    if (cost == -1) {
        cout << "-1\n";
    } else {
        cout << cost << "\n";
        // 输出所有被选择的边编号
        for (int i = 0; i < edges.size(); i++) {
            if (i > 0) cout << " ";
            cout << edges[i];
        }
        cout << "\n";
    }
    
    return 0;
}