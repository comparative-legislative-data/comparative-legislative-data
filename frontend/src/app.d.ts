// See https://svelte.dev/docs/kit/types#app.d.ts
declare global {
	namespace App {
		interface Locals {
			user: {
				user_id: number;
				email: string;
				name: string;
				role?: string;
				is_super_user: boolean;
			} | null;
		}
	}
}

export {};
