from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances.
    """

    class Meta:
        model = Product
        fields = '__all__'

    """
    Image upload field for the product.
    """
    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        """
        Initializes the form.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

    def clean_price(self):
        """
        Ensure that the price is not negative.
        """
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_rating(self):
        """
        Ensure that the rating is not negative.
        """
        rating = self.cleaned_data.get('rating')
        if rating is not None and rating < 0:
            raise forms.ValidationError("Rating cannot be negative.")
        return rating
