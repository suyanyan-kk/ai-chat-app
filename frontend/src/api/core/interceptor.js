//  ⭐ 拦截器系统
export class InterceptorManager {
  constructor() {
    this.handlers = []
  }

  use(fn) {
    this.handlers.push(fn)
  }

  async run(config) {
    let result = config
    for (const handler of this.handlers) {
      result = await handler(result)
    }
    return result
  }
}