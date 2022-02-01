<script>
	import { getCategories, getProductsByCategory } from '$lib/queries';

	async function setup() {
		const categories = await getCategories('it');

		const collection = {};

		for (let i = 0; i < categories.length; i++) {
			// Get the category
			const cat = categories[i];

			// Get the products
			const products = await getProductsByCategory(cat, 'it');

			// We save the name of the products
			const prodNames = [];
			products.forEach((p) => {
				let nome = p.fields.nome;
				nome = nome.replace('Olive', '').replace('Tarallo', '').replace('Taralli', '');
				prodNames.push(nome.toLowerCase());
			});

			collection[cat.fields.nomeCategoria] = prodNames;
		}

		return collection;
	}

	let promise = setup();
</script>

{#await promise}
	loading
{:then collection}
	<div class="cont">
		{#each Object.keys(collection) as c}
			<h3 class="break-inside"><strong>{c}</strong></h3>
			{#each collection[c] as prod}
				<div class="prod break-inside">
					<p>{prod}</p>
					<div class="cell" />
				</div>
			{/each}
		{/each}
	</div>
{/await}

<style>
	.cont {
		position: relative;
		columns: 3;
		column-fill: auto;
		height: 100vh;
	}

	p,
	h3 {
		margin: 0;
		padding: 4px 10px;
	}

	h3 {
		background-color: black;
		color: white;
	}

	.break-inside {
		-webkit-column-break-inside: avoid;
		page-break-inside: avoid;
		break-inside: avoid;
	}

	/*  */

	.prod {
		color: black;
		margin: 0;
		border: 1px solid gray;
		display: flex;
		flex-flow: row nowrap;
		align-items: stretch;
	}

	p {
		flex-grow: 1;
	}

	.cell {
		border-left: 1px solid gray;
		width: 40px;
		flex-shrink: 0 !important;
	}

	div.cont > div:nth-of-type(odd) {
		background: #ebeaea;
	}
</style>
