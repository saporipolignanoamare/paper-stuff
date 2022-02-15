<script lang="ts">
	import { getTaralli } from '$lib/queries';

	async function setup() {
		// Get the products
		const taralliReq = await getTaralli();
		const taralli = taralliReq.map((t) => {
			const nome: { it: string; en: string } = t.fields.nome as any;
			const prezzo: number = (t.fields.prezzo as any).it / 10;
			const prezzoFormat: string = prezzo.toFixed(2).replace('.', ',');
			return { it: nome.it, en: nome.en, p: prezzoFormat };
		});
		return taralli;
	}

	let promise = setup();
</script>

{#await promise}
	loading
{:then taralli}
	<div class="cont">
		{#each taralli as t}
			<div class="card">
				<div class="name-cont">
					<p class="name name-it">{t.it}</p>
					<p class="name name-en">{t.en}</p>
				</div>
				<p class="price">{t.p}€ – 100g</p>
			</div>
		{/each}
	</div>
{/await}

<style>
	.cont {
		display: flex;
		flex-flow: row wrap;
	}

	.card {
		border: 1px solid lightgray;
		width: 50vw;
		height: 25vh;

		display: flex;
		flex-flow: column nowrap;

		--s: 20px;
		--c: rgb(94, 94, 0);
	}

	p {
		margin: 0;
		font-size: 32px;
		line-height: 1;
	}

	.name-cont {
		padding: var(--s);
		flex-grow: 1;
	}

	.name-it {
		margin-bottom: 10px;
		color: var(--c);
	}

	.name-en {
		color: var(--c);
		opacity: 0.7;
	}

	.price {
		color: white;
		background-color: var(--c);
		padding: var(--s);
	}

	@media print and (orientation: landscape) {
		.card {
			width: 50vw;
			height: 50vh;
		}

		p {
			font-size: 50px;
		}

		.name-it {
			margin-bottom: var(--s);
		}
	}
</style>
