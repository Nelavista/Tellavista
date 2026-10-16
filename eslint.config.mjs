// Flat ESLint config (ESLint 9). Deliberately conservative: correctness rules only,
// no stylistic rules (Prettier owns formatting).
import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['**/dist/**', '**/.expo/**', '**/node_modules/**', '**/src/generated/**', 'app/**'] },
  ...tseslint.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    rules: {
      // Warnings, not errors: skeletons and generated code churn.
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',
      // React 17+ JSX runtime needs no React import; allow the namespace import.
      '@typescript-eslint/no-namespace': 'off',
    },
  },
);
