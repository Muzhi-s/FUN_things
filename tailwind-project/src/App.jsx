import { useState } from 'react'

function App() {
  const [isLogin, setIsLogin] = useState(true)

  return (
    <div className="flex min-h-screen items-center justify-center p-6 bg-linear-to-bl from-violet-600 via-indigo-900 to-slate-900">
      
      {/* 容器查询包裹器 */}
      <div className="@container w-full max-w-md">
        
        {/* 卡片主体 - 磨砂玻璃效果 */}
        <div className="relative overflow-hidden rounded-3xl bg-white/10 p-8 shadow-2xl backdrop-blur-2xl border border-white/20">
          
          {/* 背景装饰光斑 */}
          <div className="pointer-events-none absolute -top-24 -left-24 size-64 rounded-full bg-purple-500/30 blur-3xl"></div>
          <div className="pointer-events-none absolute -bottom-24 -right-24 size-64 rounded-full bg-pink-500/30 blur-3xl"></div>

          {/* 标题部分 */}
          <div className="text-center mb-8 relative z-10">
            <h1 className="text-3xl font-black text-white tracking-tight drop-shadow-sm">
              {isLogin ? '欢迎回来' : '加入我们'}
            </h1>
            <p className="mt-2 text-white/60 text-sm font-medium">
              {isLogin ? '请输入您的账号以继续' : '创建一个新账号开始体验'}
            </p>
          </div>

          {/* 表单部分 */}
          <form className="space-y-5 relative z-10">
            
            {/* 注册且显示名字字段 - 利用简单的条件渲染 */}
            {!isLogin && (
              <div className="group">
                <label className="block text-xs font-semibold uppercase tracking-wider text-white/70 mb-1.5 pl-1">
                  用户名
                </label>
                <input 
                  type="text" 
                  placeholder="Your Name"
                  className="w-full rounded-xl bg-black/20 border border-white/10 px-4 py-3 text-white placeholder-white/30 outline-none focus:border-purple-400/50 focus:bg-black/30 focus:shadow-[0_0_15px_rgba(168,85,247,0.15)] transition-all"
                />
              </div>
            )}

            <div className="group">
               <label className="block text-xs font-semibold uppercase tracking-wider text-white/70 mb-1.5 pl-1">
                 电子邮箱
               </label>
               <input 
                 type="email" 
                 placeholder="name@example.com"
                 className="w-full rounded-xl bg-black/20 border border-white/10 px-4 py-3 text-white placeholder-white/30 outline-none focus:border-purple-400/50 focus:bg-black/30 focus:shadow-[0_0_15px_rgba(168,85,247,0.15)] transition-all"
               />
            </div>

            <div className="group">
               <label className="block text-xs font-semibold uppercase tracking-wider text-white/70 mb-1.5 pl-1">
                 密码
               </label>
               <input 
                 type="password" 
                 placeholder="••••••••"
                 className="w-full rounded-xl bg-black/20 border border-white/10 px-4 py-3 text-white placeholder-white/30 outline-none focus:border-purple-400/50 focus:bg-black/30 focus:shadow-[0_0_15px_rgba(168,85,247,0.15)] transition-all"
               />
            </div>

            {/* 忘记密码 (仅登录) */}
            {isLogin && (
              <div className="flex justify-end">
                <a href="#" className="text-xs text-white/50 hover:text-white transition-colors">
                  忘记密码?
                </a>
              </div>
            )}

            {/* 提交按钮 */}
            <button 
              type="button"
              className="mt-2 w-full cursor-pointer rounded-xl bg-linear-to-r from-purple-500 to-indigo-500 py-3.5 font-bold text-white shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all border border-white/10"
            >
              {isLogin ? '登 录' : '注册账号'}
            </button>
          </form>

          {/* 切换模式 */}
          <div className="mt-8 text-center border-t border-white/10 pt-6 relative z-10">
            <p className="text-white/60 text-sm">
              {isLogin ? '还没有账号? ' : '已经有账号了? '}
              <button 
                onClick={() => setIsLogin(!isLogin)}
                className="font-bold text-white hover:text-purple-300 transition-colors ml-1 cursor-pointer underline underline-offset-4 decoration-white/30 hover:decoration-purple-300"
              >
                {isLogin ? '立即注册' : '直接登录'}
              </button>
            </p>
          </div>
          
        </div>
      </div>
    </div>
  )
}

export default App