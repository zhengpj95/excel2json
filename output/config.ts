/** 本文件为导表工具导出，不可手动修改 */

/** guide */
interface GuideConfig {
	/** 引导id */
	readonly index: number;
	/** 触发条件 */
	readonly trigger: number;
}

/** guide_step */
interface GuideStepConfig {
	/** 引导id */
	readonly index: number;
	/** 引导步骤 */
	readonly step: number;
	/** 引导类型 */
	readonly guide_type: number;
	/** 特效 */
	readonly effect: string;
	/** 文本在目标的那个方向 */
	readonly dir: number;
	/** 手指在目标的那个方向 */
	readonly finger_dir: number;
	/** 引导弹窗偏移 */
	readonly offset: any[];
	/** 引导文本 */
	readonly tips: string;
	/** 指引参数 */
	readonly param: any[];
}

/** 按钮配置 */
interface IconConfig {
	/** id */
	readonly id: number;
	/** 图标 */
	readonly icon: string;
	/** 常驻红点 */
	readonly rp: number;
	/** 特效 */
	readonly eff: string;
	/** 所在group */
	readonly grType: string;
}

/** 语言包 */
interface LangConfig {
	/** 名称 */
	readonly name: number;
	/** 键值 */
	readonly value: string;
	/** 值1 */
	readonly value1: any[];
	/** 值2 */
	readonly value2: any;
}

