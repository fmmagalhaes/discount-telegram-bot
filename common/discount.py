class DiscountGroup:
    def __init__(self, source, discounts):
        self.source = source
        self.discounts = discounts

    @staticmethod
    def fromJson(group_data):
        discounts = []
        for discount in group_data.get("discounts"):
            discounts.append(Discount.fromJson(discount))

        return DiscountGroup(
            group_data.get("source"),
            discounts,
        )

    def __eq__(self, other):
        return self.source == other.source


class Discount:
    def __init__(self, content):
        self.content = content

    @staticmethod
    def fromJson(discount_data):
        return Discount(
            discount_data.get("content"),
        )
