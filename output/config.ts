/** 本文件为导表工具导出，不可手动修改 */

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
