# Ubuntu 安装openclaw教程

## 前提1：处理虚拟机（Ubuntu) 连接宿主机 (Windows) 代理

### 1. 核心逻辑架构

虚拟机通过虚拟网卡（VMnet8）与宿主机通信。宿主机作为虚拟机的**网关**，运行代理软件并开启“允许局域网连接”功能，充当流量出口。

### 2. 宿主机 (Windows) 配置步骤

**A. 代理软件设置**

1. **确定端口**：确认代理软件（如 Clash/V2Ray）的 HTTP 端口（本案例为 `7897`）。

2. **开启局域网共享**：勾选 **"Allow LAN"** 或 **"允许局域网连接"**。

3. **验证监听状态**：
   打开 CMD，执行 `netstat -ano | findstr :7897`。
   
   - **必须看到**：`0.0.0.0:7897 LISTENING`（表示监听所有网卡）。

**B. 防火墙开门**

必须放行 7897 端口的入站流量，否则 Windows 会拦截虚拟机的请求。

1. 以管理员身份运行 CMD。

2. 执行命令：

```dos
netsh advfirewall firewall add rule name="Allow_VM_Proxy" dir=in action=allow protocol=TCP localport=7897
```

### 3.虚拟机 (Ubuntu) 配置步骤

**A. 定位宿主机 IP**

在 Ubuntu 终端执行：

```bash
ip route show | grep default
```

- **关键点**：通常 VMware NAT 模式下，宿主机 IP 是 `192.168.x.1`（本案例为 `192.168.186.1`）。

**B. 临时生效代理**

在终端输入以下变量（仅对当前终端有效）：

```bash
export hostip=192.168.186.1
export port=7897
export http_proxy="http://$hostip:$port"
export https_proxy="http://$hostip:$port"
```

**C. 验证连接**

```bash
export hostip=192.168.186.1
export port=7897
export http_proxy="http://$hostip:$port"
export https_proxy="http://$hostip:$port"
```

- **成功标志**：返回 `HTTP/2 200` 或 `HTTP/1.1 200 OK`。

## VS Code (Windows) 远程连接虚拟机 (Ubuntu)

**1. 环境准备 (Pre-requisites)**

- **Windows 端**：安装 VS Code，并在扩展市场安装 **Remote - SSH** 插件。

- **Ubuntu 端**：确保安装并启用了 SSH 服务：
  
  ```bash
  sudo apt update && sudo apt install -y openssh-server
  sudo systemctl enable --now ssh
  ```

**2. 身份验证**

在 VMware NAT 模式下，宿主机 IP（通常是 `.1`）和虚拟机 IP（通常是 `.128~.254`）是不同的。

- **错误操作**：连接 `.1`（这是在尝试连接 Windows 本身）。

- **正确操作**：在 Ubuntu 终端执行 `ip addr | grep 192.168`，锁定类似 `192.168.186.133` 的真实地址。

**3.服务端配置**

现代 Linux 为了安全，默认可能关闭了密码登录。

- **修改配置**：`sudo nano /etc/ssh/sshd_config`

- **去注释/修改**：将 `#PasswordAuthentication yes` 改为 `PasswordAuthentication yes`。

- **重启生效**：`sudo systemctl restart ssh`。

**4. 客户端连接：VS Code 操作流程**

1. **添加主机**：点击远程资源管理器 -> **SSH +** -> 输入 `ssh muzhi@192.168.186.133`。

2. **确认指纹**：首次连接会弹出 `Are you sure...`，必须输入 **`yes`**（这会在 Windows 的 `known_hosts` 中记录该虚拟机的身份）。

3. **输入密码**：输入 Ubuntu 用户的登录密码。

4. **选择目录**：连接成功后，点击 **Open Folder**，选择你的项目路径（如 `/home/muzhi/openclaw_project`）。



以ds为例拿到API keys

sk-8b688116a35445b7a5993ff1ddca118b





GitHub的公钥：
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIATciffi2j7r/h9+TwqsX1cniLTFzNjMCgISpD4z9LQm 2624758301@qq.com


