/** 语言包 */
interface LangConfig {
	/** 名称 */
	readonly name: number;
	/** asdfasdf */
	readonly value: string;
	/** 12312312 */
	readonly value1: any[];
	/** as和12hi是1 */
	readonly value2: any;
}

/** xxx配置 */
interface AchievementConfig {
	/**成就阶数*/
	readonly order_level: number;
	/** 1阶数奖励1a */
	readonly rewards: number[][];
	/**达标阶数所需积分123*/
	readonly value: number;
}

/** yyy配置 */
interface ActiveAwardConfig {
	/**__奖励ID*/
	readonly index: number;
	/**啊啊123123需要历练值*/
	readonly activation: number;
	/**奖励内容123123*/
	readonly award: number[][];
}
