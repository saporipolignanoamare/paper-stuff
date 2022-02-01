import { client } from './client';
import type { ICategoria, IProdotto } from './types';

//

export async function getCategories(locale: string): Promise<Array<ICategoria>> {
	// Requesting categories
	const data = await client.getEntries({
		content_type: 'categoria',
		locale
	});
	// Casting type
	let categories = data.items as Array<ICategoria>;
	// Sorting
	categories = categories.sort(sortCategories);
	//
	return categories;
}

function sortCategories(a: ICategoria, b: ICategoria) {
	return a.fields.ordine - b.fields.ordine;
}

//

export async function getProducts(): Promise<Array<IProdotto>> {
	// Requesting categories
	const data = await client.getEntries({
		content_type: 'prodotto'
	});
	// Casting type
	return data.items as Array<IProdotto>;
}

export async function getProductsByCategory(
	category: ICategoria,
	locale: string
): Promise<Array<IProdotto>> {
	// Requesting categories
	const data = await client.getEntries({
		content_type: 'prodotto',
		'fields.categoria.sys.id': category.sys.id,
		locale
	});
	// Casting type
	return data.items as Array<IProdotto>;
}
